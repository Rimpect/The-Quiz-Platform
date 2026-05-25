import React, { useState } from 'react'

import { Button, ModalHelp } from '@shared'
import { CircleQuestionMark } from 'lucide-react'

export function QuizHelp() {
  const [isHelpModalOpen, setIsHelpModalOpen] = useState(false)
  return (
    <div>
      <Button
        variant="white"
        size="medium"
        icon={<CircleQuestionMark size={20} />}
        onClick={() => setIsHelpModalOpen(true)}
      >
        Помощь
      </Button>
      {isHelpModalOpen && (
        <ModalHelp onClose={() => setIsHelpModalOpen(false)} />
      )}
    </div>
  )
}
