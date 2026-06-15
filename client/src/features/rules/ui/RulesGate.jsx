import React, { useState } from 'react'

import { useNavigate } from 'react-router-dom'

import { RulesModal } from './RulesModal'

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
      <RulesModal isOpen onAccept={handleAccept} onDecline={handleDecline} />
    )
  }

  return children
}
