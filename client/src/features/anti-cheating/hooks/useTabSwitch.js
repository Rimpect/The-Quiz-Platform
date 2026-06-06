import { useEffect, useState, useCallback } from 'react'

export const useTabSwitch = ({ onSwitch, enabled = true } = {}) => {
  const [isTabActive, setIsTabActive] = useState(true)
  const [switchCount, setSwitchCount] = useState(0)

  const handleVisibilityChange = useCallback(() => {
    const isVisible = document.visibilityState === 'visible'

    if (!isVisible && enabled) {
      setSwitchCount((prev) => prev + 1)
      if (onSwitch) onSwitch()
    }

    setIsTabActive(isVisible)
  }, [onSwitch, enabled])

  useEffect(() => {
    if (!enabled) return

    document.addEventListener('visibilitychange', handleVisibilityChange)

    return () => {
      document.removeEventListener('visibilitychange', handleVisibilityChange)
    }
  }, [handleVisibilityChange, enabled])

  return { isTabActive, switchCount }
}
