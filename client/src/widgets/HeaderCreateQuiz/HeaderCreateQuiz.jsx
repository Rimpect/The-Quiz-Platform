import React from 'react'
import { MoveLeft, CircleQuestionMark, Save } from 'lucide-react'
import { Button } from '@shared'
import { Link } from 'react-router-dom'

import styles from './HeaderCreateQuiz.module.scss'

export function HeaderCreateQuiz() {
  return (
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
        >
          Помощь
        </Button>
        <Button variant="black" size="medium" icon={<Save size={20} />}>
          Сохранить квиз
        </Button>
      </div>
    </div>
  )
}
