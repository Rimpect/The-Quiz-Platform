import { useEffect, useRef } from 'react'

export const useDevTools = ({ enabled = true, onDetect } = {}) => {
  const checkInterval = useRef(null)

  useEffect(() => {
    if (!enabled) return

    const detectDevTools = () => {
      const threshold = 160
      const widthThreshold = window.outerWidth - window.innerWidth > threshold
      const heightThreshold =
        window.outerHeight - window.innerHeight > threshold

      if (widthThreshold || heightThreshold) {
        if (onDetect) onDetect()
      }
    }

    checkInterval.current = setInterval(detectDevTools, 1000)

    return () => {
      if (checkInterval.current) {
        clearInterval(checkInterval.current)
      }
    }
  }, [enabled, onDetect])
}
