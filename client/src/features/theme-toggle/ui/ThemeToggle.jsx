import { useState } from 'react'

import { Button } from '@shared'
import { Moon, Sparkles, Sun } from 'lucide-react'
import { toast } from 'sonner'

import styles from './ThemeToggle.module.scss'

export function ThemeToggle() {
  const [isDarkTheme, setIsDarkTheme] = useState(false)
  const [isAnimating, setIsAnimating] = useState(false)
  const [showSparkles, setShowSparkles] = useState(false)

  const handleThemeToggle = () => {
    setIsAnimating(true)
    setShowSparkles(true)

    setTimeout(() => {
      const nextTheme = !isDarkTheme

      setIsDarkTheme(nextTheme)

      toast.success(nextTheme ? '🌙 Темная тема' : '☀️ Светлая тема', {
        description: nextTheme
          ? 'Темная тема активирована'
          : 'Светлая тема активирована',
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
