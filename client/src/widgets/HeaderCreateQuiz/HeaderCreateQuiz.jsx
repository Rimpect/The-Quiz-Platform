import React, { useState } from 'react'

import { Button, ModalHelp } from '@shared'
import { MoveLeft, CircleQuestionMark, Save } from 'lucide-react'
import { Link } from 'react-router-dom'
import { toast } from 'sonner'

import styles from './HeaderCreateQuiz.module.scss'

export function HeaderCreateQuiz() {
  const [isHelpModalOpen, setIsHelpModalOpen] = useState(false)
  const saveClick = () => {
    toast.error('Ошибка при сохранении', {
      description: 'Эта функция еще не доработана',
    })
  }
  return (
    <>
      <div className={styles.header}>
        <Link to="/MainPage">
          <Button
            variant="transparent"
            size="medium"
            icon={<MoveLeft size={20} />}
          >
            Назад
          </Button>
        </Link>
        <div className={styles.buttons}>
          <Button
            variant="white"
            size="medium"
            icon={<CircleQuestionMark size={20} />}
            onClick={() => setIsHelpModalOpen(true)}
          >
            Помощь
          </Button>
          <Button
            onClick={saveClick}
            variant="black"
            size="medium"
            icon={<Save size={20} />}
          >
            Сохранить квиз
          </Button>
        </div>
      </div>
      {isHelpModalOpen && (
        <ModalHelp onClose={() => setIsHelpModalOpen(false)} />
      )}
    </>
  )
}
