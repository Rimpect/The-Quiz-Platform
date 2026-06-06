import { useEffect, useCallback } from 'react'

export const useCopyPaste = ({ enabled = true, onViolation } = {}) => {
  const handleCopyPaste = useCallback(
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

    document.addEventListener('copy', handleCopyPaste)
    document.addEventListener('paste', handleCopyPaste)
    document.addEventListener('cut', handleCopyPaste)

    return () => {
      document.removeEventListener('copy', handleCopyPaste)
      document.removeEventListener('paste', handleCopyPaste)
      document.removeEventListener('cut', handleCopyPaste)
    }
  }, [handleCopyPaste, enabled])
}
