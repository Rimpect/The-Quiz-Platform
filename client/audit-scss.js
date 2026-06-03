const fs = require('fs')
const path = require('path')
const glob = require('glob')
const root = process.cwd()
const modules = glob.sync('src/**/*.module.scss')
for (const file of modules) {
  const content = fs.readFileSync(path.join(root, file), 'utf8')
  const defined = new Set()
  const re = /\.(?:[A-Za-z0-9_-]+)/g
  let m
  while ((m = re.exec(content))) defined.add(m[0].slice(1))
  const jsFiles = glob
    .sync(file.replace(/\.module\.scss$/, '.js'), { cwd: root })
    .concat(glob.sync(file.replace(/\.module\.scss$/, '.jsx'), { cwd: root }))
    .concat(glob.sync(file.replace(/\.module\.scss$/, '.ts'), { cwd: root }))
    .concat(glob.sync(file.replace(/\.module\.scss$/, '.tsx'), { cwd: root }))
  const used = new Set()
  const scanFiles = jsFiles.length
    ? jsFiles
    : glob.sync('src/**/*.{js,jsx,ts,tsx}', { cwd: root, nodir: true })
  for (const jsFile of scanFiles) {
    const contentJS = fs.readFileSync(path.join(root, jsFile), 'utf8')
    if (!jsFiles.length || contentJS.includes(file)) {
      const reUse = /styles\.([A-Za-z0-9_-]+)/g
      let mm
      while ((mm = reUse.exec(contentJS))) used.add(mm[1])
    }
  }
  const definedArr = Array.from(defined).sort()
  const usedArr = Array.from(used).sort()
  const extra = usedArr.filter((x) => !defined.has(x))
  const unused = definedArr.filter((x) => !used.has(x))
  if (extra.length || unused.length) {
    console.log(file)
    if (extra.length) console.log(' used not defined:', extra.join(', '))
    if (unused.length)
      console.log(
        ' defined not used:',
        unused.slice(0, 20).join(', ') +
          (unused.length > 20 ? ` (+${unused.length - 20})` : ''),
      )
    console.log('---')
  }
}
