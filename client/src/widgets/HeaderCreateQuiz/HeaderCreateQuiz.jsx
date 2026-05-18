import React from 'react'

import { Button } from '@shared'
import { Link } from 'react-router-dom'

import styles from './HeaderCreateQuiz.module.scss'

export function HeaderCreateQuiz() {
  return (
    <div className={styles.header}>
      <Link>
        <Button>назад</Button>
      </Link>
      <div className={styles.buttons}>
        <Button>Помощь</Button>
        <Button>Сохранить квиз</Button>
      </div>
    </div>
  )
}
