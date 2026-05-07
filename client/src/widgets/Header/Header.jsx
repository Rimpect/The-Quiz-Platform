import { useState } from 'react'

import { User, Shield, Sun, Moon } from 'lucide-react'
import { Link } from 'react-router-dom'

import styles from './Header.module.scss'

export function Header() {
  const [isTheme, setTheme] = useState('white')
  return (
    <header className={styles.headerContainer}>
      <div className={styles.headerInner}>
        <div className={styles.logo}>
          <div className={styles.logoIcon}>Q</div>
          <div className={styles.logoTitle}>QuizMaster</div>
        </div>
        <div className={styles.user}>
          <button
            onClick={() => setTheme(!isTheme)}
            className={styles.adminButton}
          >
            {isTheme ? <Sun size={24} /> : <Moon size={24} />}
          </button>

          <Link to="/AdminPanel" className={styles.userLink}>
            <span className={styles.adminButton}>
              <Shield />
              Админка
            </span>
          </Link>
          <User className={styles.userIcon} />
          <span className={styles.userText}>Имя пользователя/Гость</span>
          <Link to="/PersonalAccount" className={styles.userLink}>
            <span className={styles.userButton}>Войти</span>
          </Link>
        </div>
      </div>
    </header>
  )
}
