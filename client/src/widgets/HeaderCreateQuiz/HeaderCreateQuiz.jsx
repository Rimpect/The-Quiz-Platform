import { QuizHelp, SaveQuiz } from '@features'
import { Button, ROUTES } from '@shared'
import { MoveLeft } from 'lucide-react'
import { Link } from 'react-router-dom'

import styles from './HeaderCreateQuiz.module.scss'

export function HeaderCreateQuiz() {
  return (
    <>
      <div className={styles.header}>
        <Link to={ROUTES.main}>
          <Button
            variant="transparent"
            size="medium"
            icon={<MoveLeft size={20} />}
          >
            Назад
          </Button>
        </Link>
        <div className={styles.buttons}>
          <QuizHelp />
          <SaveQuiz />
        </div>
      </div>
    </>
  )
}
