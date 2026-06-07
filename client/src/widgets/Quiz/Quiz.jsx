import React from 'react'

import { AntiCheatProvider } from '@features/anti-cheating'
import { useNavigate, useParams } from 'react-router-dom'

import { QuizContent } from './QuizContent'

export function Quiz() {
  const { id } = useParams()
  const navigate = useNavigate()

  const handleDecline = () => {
    navigate(-1)
  }

  return (
    <AntiCheatProvider
      quizId={id}
      onDecline={handleDecline}
      config={{
        maxWarnings: 3,
        autoSubmitOnViolation: false,
        blockCopyPaste: true,
        blockDevTools: true,
      }}
    >
      <QuizContent quizId={id} />
    </AntiCheatProvider>
  )
}
