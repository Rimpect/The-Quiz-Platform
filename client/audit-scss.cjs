/**
 * Поиск и удаление неиспользуемых CSS-классов в *.module.scss.
 *
 *   node audit-scss.cjs            # dry-run: показать что будет удалено
 *   node audit-scss.cjs --write    # удалить
 *
 * Консервативно: удаляет ТОЛЬКО top-level правила, у которых ВСЕ селекторы —
 * простые одиночные классы (`.foo`, `.a, .b`) и ни один не используется в JS.
 * Пропускает: элементные/составные/псевдо/`&` селекторы, @media/@mixin и т.п.,
 * файлы с динамическим доступом `styles[...]`, scss без потребителей.
 * Учитывает scss-цепочки @import/@use (классы шарятся между файлами).
 */
const fs = require('fs')
const path = require('path')

const glob = require('glob')
const scssSyntax = require('postcss-scss')

const root = process.cwd()
const WRITE = process.argv.includes('--write')

// ---- 1. JS-файлы: импорты scss и использование классов ----
const jsFiles = glob.sync('src/**/*.{js,jsx,ts,tsx}', { cwd: root, nodir: true })
const jsContent = new Map()
const scssImportedByJs = new Map() // scssAbs -> [jsAbs...]
const importScssRe = /from\s+['"]([^'"]+\.module\.scss)['"]/g

for (const rel of jsFiles) {
  const abs = path.join(root, rel)
  const content = fs.readFileSync(abs, 'utf8')
  jsContent.set(abs, content)
  let m
  while ((m = importScssRe.exec(content))) {
    if (!m[1].startsWith('.')) continue
    const scssAbs = path.resolve(path.dirname(abs), m[1])
    if (!scssImportedByJs.has(scssAbs)) scssImportedByJs.set(scssAbs, [])
    scssImportedByJs.get(scssAbs).push(abs)
  }
}

// ---- 2. scss-цепочки @import/@use (.module.scss шарят классы) ----
const modules = glob.sync('src/**/*.module.scss', { cwd: root })
const scssImportsScss = new Map() // scssAbs -> Set(scssAbs)
const importInScssRe = /@(?:import|use|forward)\s+['"]([^'"]+)['"]/g

for (const rel of modules) {
  const abs = path.join(root, rel)
  const css = fs.readFileSync(abs, 'utf8')
  const set = new Set()
  let m
  while ((m = importInScssRe.exec(css))) {
    const spec = m[1]
    if (!spec.includes('.module') || !spec.startsWith('.')) continue
    let resolved = path.resolve(path.dirname(abs), spec)
    if (!resolved.endsWith('.scss')) resolved += '.module.scss'
    set.add(resolved)
  }
  scssImportsScss.set(abs, set)
}

// reverse: какие scss @import-ят данный scss
const scssImportedByScss = new Map()
for (const [importer, set] of scssImportsScss) {
  for (const imported of set) {
    if (!scssImportedByScss.has(imported)) scssImportedByScss.set(imported, new Set())
    scssImportedByScss.get(imported).add(importer)
  }
}

// Все JS-потребители scss с учётом scss-цепочек
function getConsumers(scssAbs) {
  const result = new Set()
  const seen = new Set()
  const stack = [scssAbs]
  while (stack.length) {
    const cur = stack.pop()
    if (seen.has(cur)) continue
    seen.add(cur)
    for (const js of scssImportedByJs.get(cur) || []) result.add(js)
    for (const importer of scssImportedByScss.get(cur) || []) stack.push(importer)
  }
  return [...result]
}

// ---- 3. Анализ каждого scss ----
const usedRe = /styles\.([A-Za-z0-9_]+)|styles\[\s*['"]([A-Za-z0-9_-]+)['"]\s*\]/g
const dynamicRe = /styles\[\s*[^'"\]]/ // styles[variable] — динамика
const simpleClassRe = /^\.[A-Za-z0-9_-]+$/

let totalRemoved = 0
const orphans = []
const skipped = []

for (const rel of modules) {
  const abs = path.join(root, rel)
  const consumers = getConsumers(abs)
  if (consumers.length === 0) {
    orphans.push(rel)
    continue
  }

  let dynamic = false
  const used = new Set()
  for (const c of consumers) {
    const content = jsContent.get(c) || ''
    if (dynamicRe.test(content)) dynamic = true
    let m
    usedRe.lastIndex = 0
    while ((m = usedRe.exec(content))) used.add(m[1] || m[2])
  }
  if (dynamic) {
    skipped.push(rel + ' (динамический styles[...])')
    continue
  }

  const css = fs.readFileSync(abs, 'utf8')
  // классы, на которые ссылаются внутри scss через @extend — тоже used
  let e
  const extendRe = /@extend\s+\.([A-Za-z0-9_-]+)/g
  while ((e = extendRe.exec(css))) used.add(e[1])

  let rootNode
  try {
    rootNode = scssSyntax.parse(css)
  } catch {
    skipped.push(rel + ' (parse error)')
    continue
  }

  const toRemove = []
  rootNode.each((node) => {
    if (node.type !== 'rule') return // только top-level правила
    const selectors = node.selector
      .split(',')
      .map((s) => s.trim())
      .filter(Boolean)
    const allSimple =
      selectors.length > 0 && selectors.every((s) => simpleClassRe.test(s))
    if (!allSimple) return
    const names = selectors.map((s) => s.slice(1))
    if (names.every((n) => !used.has(n))) toRemove.push({ node, names })
  })

  if (!toRemove.length) continue

  console.log(rel)
  for (const r of toRemove) console.log('  - .' + r.names.join(', .'))
  totalRemoved += toRemove.length

  if (WRITE) {
    toRemove.forEach((r) => r.node.remove())
    fs.writeFileSync(abs, rootNode.toString(), 'utf8')
  }
}

console.log(
  '\n' +
    (WRITE ? 'УДАЛЕНО' : 'НАЙДЕНО (dry-run)') +
    ' неиспользуемых правил: ' +
    totalRemoved,
)
if (orphans.length)
  console.log(
    '\nscss без JS-потребителей (НЕ трогаю, проверь вручную): ' +
      orphans.length +
      '\n  ' +
      orphans.join('\n  '),
  )
if (skipped.length)
  console.log('\nпропущено: ' + skipped.length + '\n  ' + skipped.join('\n  '))
if (!WRITE) console.log('\nЧтобы удалить: node audit-scss.cjs --write')
