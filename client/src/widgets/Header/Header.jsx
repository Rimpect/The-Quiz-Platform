import { useState } from 'react'

import { Button, ROUTES } from '@shared'
import { User, Shield, Sun, Moon, Sparkles } from 'lucide-react'
import { Link } from 'react-router-dom'
import { toast } from 'sonner'

import styles from './Header.module.scss'

export function Header() {
  const [isTheme, setTheme] = useState(false)
  const [isAnimating, setIsAnimating] = useState(false)
  const [showSparkles, setShowSparkles] = useState(false)

  const handleThemeToggle = () => {
    setIsAnimating(true)
    setShowSparkles(true)

    setTimeout(() => {
      setTheme(!isTheme)

      toast.success(isTheme ? '🌞 Светлая тема' : '🌙 Темная тема', {
        description: isTheme
          ? 'Светлая тема активирована'
          : 'Темная тема активирована',
        duration: 1500,
        icon: isTheme ? '☀️' : '🌙',
      })

      setTimeout(() => {
        setIsAnimating(false)
        setShowSparkles(false)
      }, 300)
    }, 150)
  }

  return (
    <header
      className={`${styles.headerContainer} ${isTheme ? styles.darkTheme : styles.lightTheme}`}
    >
      <div className={styles.headerInner}>
        <div className={styles.logo}>
          <div className={styles.logoIcon}>
            <Link to={ROUTES.main} className={styles.userLink}>
              Q
            </Link>
          </div>
          <div className={styles.logoTitle}>QuizMaster</div>
        </div>
        <div className={styles.user}>
          <div className={styles.themeButtonWrapper}>
            {showSparkles && (
              <div className={styles.sparkles}>
                <Sparkles size={16} className={styles.sparkle1} />
                <Sparkles size={12} className={styles.sparkle2} />
                <Sparkles size={14} className={styles.sparkle3} />
              </div>
            )}
            <Button
              onClick={handleThemeToggle}
              variant="white"
              size="medium"
              icon={isTheme ? <Sun size={20} /> : <Moon size={20} />}
              className={`${styles.themeButton} ${isAnimating ? styles.rotate : ''} ${styles.headerButton}`}
            />
          </div>
          <Link to={ROUTES.admin} className={styles.userLink}>
            <Button
              variant="white"
              size="medium"
              icon={<Shield size={20} />}
              className={styles.headerButton}
            >
              Админка
            </Button>
          </Link>
          <User className={styles.userIcon} />
          <span className={styles.userText}>Имя пользователя/Гость</span>
          <Link to={ROUTES.profile} className={styles.userLink}>
            <Button
              variant="white"
              size="medium"
              className={styles.headerButton}
            >
              Войти
            </Button>
          </Link>
        </div>
      </div>
    </header>
  )
}
