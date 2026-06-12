import React, { useState } from 'react'

import { useNavigate } from 'react-router-dom'

import { RulesModal } from './RulesModal'

/**
 * Показывает правила анти-чита перед отображением содержимого (например, лобби).
 * После согласия выставляет флаг `agreed_quiz_{quizId}` в sessionStorage,
 * поэтому при старте самого квиза правила повторно не показываются,
 * но флаг не живёт вечно — сбрасывается при закрытии вкладки.
 */
export function RulesGate({ quizId, children }) {
  const navigate = useNavigate()
  const agreedKey = `agreed_quiz_${quizId}`
  const [accepted, setAccepted] = useState(
    () => !!sessionStorage.getItem(agreedKey),
  )

  const handleAccept = () => {
    sessionStorage.setItem(agreedKey, 'true')
    setAccepted(true)
  }

  const handleDecline = () => {
    navigate(-1)
  }

  if (!accepted) {
    return (
      <RulesModal
        isOpen
        onAccept={handleAccept}
        onDecline={handleDecline}
      />
    )
  }

  return children
}
