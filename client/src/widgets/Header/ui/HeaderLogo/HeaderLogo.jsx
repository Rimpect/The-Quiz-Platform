import React from 'react'

import { ROUTES } from '@shared'
import { Link } from 'react-router-dom'

import styles from './HeaderLogo.module.scss'

export function HeaderLogo() {
  return (
    <div>
      <div className={styles.logo}>
        <div className={styles.logoIcon}>
          <Link to={ROUTES.main}>Q</Link>
        </div>
        <div>QuizMaster</div>
      </div>
    </div>
  )
}
