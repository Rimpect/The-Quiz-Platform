import { useEffect, useCallback } from 'react'

export const useKeyboardBlocker = ({ enabled = true, onViolation } = {}) => {
  const handleKeyDown = useCallback(
    (e) => {
      if (!enabled) return

      const isMac = navigator.platform.toUpperCase().indexOf('MAC') >= 0
      const cmdOrCtrl = isMac ? e.metaKey : e.ctrlKey

      // Блокируемые комбинации клавиш
      const blockedCombos = [
        // DevTools
        e.key === 'F12',
        e.ctrlKey && e.shiftKey && e.key === 'I',
        e.ctrlKey && e.shiftKey && e.key === 'C',
        e.ctrlKey && e.shiftKey && e.key === 'J',
        e.ctrlKey && e.key === 'U',

        // Скриншоты
        e.key === 'PrintScreen',
        cmdOrCtrl && e.key === 'PrintScreen',
        cmdOrCtrl && e.shiftKey && e.key === 'S',
        cmdOrCtrl && e.key === 'S',

        // Специальные для macOS
        isMac && e.metaKey && e.shiftKey && e.key === '3',
        isMac && e.metaKey && e.shiftKey && e.key === '4',
        isMac && e.metaKey && e.key === '5',

        // Специальные для Windows
        e.ctrlKey && e.key === 'PrintScreen',
        e.ctrlKey && e.altKey && e.key === 'PrintScreen',

        // Блокировка копирования и вставки
        cmdOrCtrl && e.key === 'c',
        cmdOrCtrl && e.key === 'v',
        cmdOrCtrl && e.key === 'x',
      ]

      if (blockedCombos.some(Boolean)) {
        e.preventDefault()
        if (onViolation) onViolation()
        return false
      }
    },
    [enabled, onViolation],
  )

  useEffect(() => {
    if (!enabled) return

    document.addEventListener('keydown', handleKeyDown)

    return () => {
      document.removeEventListener('keydown', handleKeyDown)
    }
  }, [handleKeyDown, enabled])
}
