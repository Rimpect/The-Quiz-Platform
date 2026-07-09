// Демо-режим: статичная сборка без бэкенда (для GitHub Pages).
// Включается переменной сборки VITE_DEMO=true. В обычной сборке всё работает как раньше.
export const IS_DEMO = import.meta.env.VITE_DEMO === 'true'

// Ссылка на полную версию (VPS) — показывается в демо-баннере.
export const FULL_VERSION_URL =
  import.meta.env.VITE_FULL_VERSION_URL ||
  'https://github.com/Rimpect/The-Quiz-Platform'

// Ссылка на репозиторий — тоже в баннере.
export const REPO_URL = 'https://github.com/Rimpect/The-Quiz-Platform'
