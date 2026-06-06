import { useState } from 'react'

import { ANTI_CHEAT_CONFIG } from '../constants/antiCheat.constants.js'

import { useCopyPaste } from './useCopyPaste'
import { useDevTools } from './useDevTools'
import { useTabSwitch } from './useTabSwitch'

export const useAntiCheat = (config = {}) => {
  const settings = { ...ANTI_CHEAT_CONFIG.DEFAULT_SETTINGS, ...config }

  const [violations, setViolations] = useState([])
  const [isBlocked, setIsBlocked] = useState(false)

  const handleViolation = (type) => {
    if (isBlocked) return

    setViolations((prev) => {
      const newViolations = [...prev, type]

      if (newViolations.length >= settings.maxWarnings) {
        setIsBlocked(true)
      }

      return newViolations
    })
  }

  const { isTabActive, switchCount } = useTabSwitch({
    enabled: true,
    onSwitch: () => handleViolation('tab_switch'),
  })

  useCopyPaste({
    enabled: settings.blockCopyPaste,
    onViolation: () => handleViolation('copy_paste'),
  })

  useDevTools({
    enabled: settings.blockDevTools,
    onDetect: () => handleViolation('dev_tools'),
  })

  return {
    violations,
    isBlocked,
    switchCount,
    isTabActive,
    violationsCount: violations.length,
    reset: () => {
      setViolations([])
      setIsBlocked(false)
    },
  }
}
