import { useEffect, useCallback } from 'react'

export const useContextMenuBlocker = ({ enabled = true, onViolation } = {}) => {
  const handleContextMenu = useCallback(
    (e) => {
      if (!enabled) return

      e.preventDefault()
      if (onViolation) onViolation()
      return false
    },
    [enabled, onViolation],
  )

  useEffect(() => {
    if (!enabled) return

    document.addEventListener('contextmenu', handleContextMenu)

    return () => {
      document.removeEventListener('contextmenu', handleContextMenu)
    }
  }, [handleContextMenu, enabled])
}
