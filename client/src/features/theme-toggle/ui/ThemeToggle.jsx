import { useState } from 'react'

import { Button } from '@shared'
import { Moon, Sparkles, Sun } from 'lucide-react'
import { toast } from 'sonner'

import useTheme from '../hooks/useTheme'
import styles from './ThemeToggle.module.scss'

export function ThemeToggle() {
  const { isDarkTheme, toggleTheme } = useTheme()
  const [isAnimating, setIsAnimating] = useState(false)
  const [showSparkles, setShowSparkles] = useState(false)

  const handleThemeToggle = () => {
    setIsAnimating(true)
    setShowSparkles(true)

    setTimeout(() => {
      toggleTheme()

      toast.success(isDarkTheme ? '☀️ Светлая тема' : '🌙 Темная тема', {
        description: isDarkTheme
          ? 'Светлая тема активирована'
          : 'Темная тема активирована',
        duration: 1500,
      })

      setTimeout(() => {
        setIsAnimating(false)
        setShowSparkles(false)
      }, 300)
    }, 150)
  }

  return (
    <div className={styles.themeButtonWrapper}>
      {showSparkles && (
        <div className={styles.sparkles}>
          <Sparkles size={16} className={styles.sparkle1} />
          <Sparkles size={12} className={styles.sparkle2} />
          <Sparkles size={14} className={styles.sparkle3} />
        </div>
      )}

      <Button
        variant="white"
        size="medium"
        onClick={handleThemeToggle}
        icon={isDarkTheme ? <Sun size={20} /> : <Moon size={20} />}
        className={`
          ${styles.themeButton}
          ${isAnimating ? styles.rotate : ''}
        `}
      />
    </div>
  )
}
