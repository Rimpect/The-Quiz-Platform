import { useEffect, useState } from 'react'

const useTheme = () => {
  const [isDarkTheme, setIsDarkTheme] = useState(() => {
    const savedTheme = localStorage.getItem('theme')
    return savedTheme === 'dark-theme'
  })

  useEffect(() => {
    const root = window.document.documentElement
    const themeClass = isDarkTheme ? 'dark-theme' : 'light-theme'

    root.classList.remove('light-theme', 'dark-theme')
    root.classList.add(themeClass)
    localStorage.setItem('theme', themeClass)
  }, [isDarkTheme])

  const toggleTheme = () => {
    setIsDarkTheme((prev) => !prev)
  }

  return { isDarkTheme, toggleTheme }
}

export default useTheme
