import { createContext, useState, useEffect, useCallback } from 'react'

import { RulesModal } from '../../rules'

// eslint-disable-next-line react-refresh/only-export-components
export const AntiCheatContext = createContext(null)

export const AntiCheatProvider = ({
  children,
  quizId,
  config = {},
  onDecline,
}) => {
  const [violations, setViolations] = useState([])
  const [isBlocked, setIsBlocked] = useState(false)
  const [quizStarted, setQuizStarted] = useState(false)

  // Проверяем согласился ли уже пользователь на этот квиз (в рамках вкладки).
  // sessionStorage, а не localStorage — флаг не должен жить вечно между сессиями.
  const hasAgreedKey = `agreed_quiz_${quizId}`
  const hasAlreadyAgreed = sessionStorage.getItem(hasAgreedKey)
  const [showRules, setShowRules] = useState(!hasAlreadyAgreed)

  // Если уже согласился раньше, сразу начинаем квиз
  useEffect(() => {
    if (hasAlreadyAgreed) {
      setQuizStarted(true)
    }
  }, [hasAlreadyAgreed])

  const defaultConfig = {
    maxWarnings: 3,
    autoSubmitOnViolation: true,
    blockCopyPaste: true,
    blockDevTools: true,
  }

  const settings = { ...defaultConfig, ...config }

  const isAntiCheatActive = quizStarted && !isBlocked

  const addViolation = useCallback(
    (type) => {
      if (!isAntiCheatActive) return

      setViolations((prev) => {
        const newViolations = [...prev, type]
        if (newViolations.length >= settings.maxWarnings) {
          setIsBlocked(true)
        }
        return newViolations
      })
    },
    [isAntiCheatActive, settings.maxWarnings],
  )

  // Запуск квиза после согласия
  const startQuiz = () => {
    setShowRules(false)
    setQuizStarted(true)
    setViolations([])
    setIsBlocked(false)
    // Сохраняем что пользователь согласился на этот квиз (в рамках вкладки)
    sessionStorage.setItem(hasAgreedKey, 'true')
  }

  // Отмена квиза
  const cancelQuiz = () => {
    setShowRules(false)
    if (onDecline) onDecline()
  }

  // Отслеживание переключения вкладок
  useEffect(() => {
    if (!isAntiCheatActive) return

    const handleVisibilityChange = () => {
      const isVisible = document.visibilityState === 'visible'
      if (!isVisible) {
        addViolation('tab_switch')
      }
    }

    document.addEventListener('visibilitychange', handleVisibilityChange)
    return () =>
      document.removeEventListener('visibilitychange', handleVisibilityChange)
  }, [isAntiCheatActive, addViolation])

  // Блокировка копирования/вставки
  useEffect(() => {
    if (!isAntiCheatActive || !settings.blockCopyPaste) return

    const handleCopyPaste = (e) => {
      e.preventDefault()
      addViolation('copy_paste')
      return false
    }

    document.addEventListener('copy', handleCopyPaste)
    document.addEventListener('paste', handleCopyPaste)
    document.addEventListener('cut', handleCopyPaste)

    return () => {
      document.removeEventListener('copy', handleCopyPaste)
      document.removeEventListener('paste', handleCopyPaste)
      document.removeEventListener('cut', handleCopyPaste)
    }
  }, [isAntiCheatActive, settings.blockCopyPaste, addViolation])

  // Блокировка клавиатурных сокращений
  useEffect(() => {
    if (!isAntiCheatActive || !settings.blockDevTools) return

    const handleKeyDown = (e) => {
      const blockedKeys = [
        e.key === 'F12',
        e.ctrlKey && e.shiftKey && e.key === 'I',
        e.ctrlKey && e.shiftKey && e.key === 'C',
        e.ctrlKey && e.key === 'U',
      ]

      if (blockedKeys.some(Boolean)) {
        e.preventDefault()
        addViolation('dev_tools')
        return false
      }
    }

    document.addEventListener('keydown', handleKeyDown)
    return () => document.removeEventListener('keydown', handleKeyDown)
  }, [isAntiCheatActive, settings.blockDevTools, addViolation])

  // Детект DevTools
  useEffect(() => {
    if (!isAntiCheatActive || !settings.blockDevTools) return

    const detectDevTools = () => {
      const widthThreshold = window.outerWidth - window.innerWidth > 160
      const heightThreshold = window.outerHeight - window.innerHeight > 160

      if (widthThreshold || heightThreshold) {
        addViolation('dev_tools')
      }
    }

    const interval = setInterval(detectDevTools, 2000)
    return () => clearInterval(interval)
  }, [isAntiCheatActive, settings.blockDevTools, addViolation])

  const contextValue = {
    isActive: isAntiCheatActive,
    violationsCount: violations.length,
    violations,
    isBlocked,
    startQuiz,
    quizStarted,
  }

  return (
    <AntiCheatContext.Provider value={contextValue}>
      <RulesModal
        isOpen={showRules}
        onAccept={startQuiz}
        onDecline={cancelQuiz}
      />
      {quizStarted && !showRules && children}
    </AntiCheatContext.Provider>
  )
}
