import { useState } from 'react'

import { Button } from '@shared'
import { User, Shield, Sun, Moon } from 'lucide-react'
import { Link } from 'react-router-dom'

import styles from './Header.module.scss'

export function Header() {
  const [isTheme, setTheme] = useState('white')
  return (
    <header className={styles.headerContainer}>
      <div className={styles.headerInner}>
        <div className={styles.logo}>
          <div className={styles.logoIcon}>
            {' '}
            <Link to="/MainPage" className={styles.userLink}>
              Q
            </Link>
          </div>
          <div className={styles.logoTitle}>QuizMaster</div>
        </div>
        <div className={styles.user}>
          <Button
            onClick={() => setTheme(!isTheme)}
            variant="white"
            size="medium"
            icon={isTheme ? <Sun size={20} /> : <Moon size={20} />}
          />
          <Link to="/AdminPanel" className={styles.userLink}>
            <Button variant="white" size="medium" icon={<Shield size={20} />}>
              Админка
            </Button>
          </Link>
          <User className={styles.userIcon} />
          <span className={styles.userText}>Имя пользователя/Гость</span>
          <Link to="/PersonalAccount" className={styles.userLink}>
            <Button variant="white" size="medium">
              Войти
            </Button>
          </Link>
        </div>
      </div>
    </header>
  )
}
