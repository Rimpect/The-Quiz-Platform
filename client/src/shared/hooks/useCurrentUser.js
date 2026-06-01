import { useState, useEffect } from 'react'

export function useCurrentUser() {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    try {
      const storedUser = localStorage.getItem('user')

      if (storedUser && storedUser !== 'undefined' && storedUser !== 'null') {
        const parsedUser = JSON.parse(storedUser)

        // Проверяем, что парсинг дал объект
        if (parsedUser && typeof parsedUser === 'object') {
          setUser(parsedUser)
        } else {
          // Если данные некорректные - удаляем
          localStorage.removeItem('user')
          setUser(null)
        }
      }
    } catch (error) {
      console.error('Ошибка парсинга пользователя:', error)
      // Удаляем поврежденные данные
      localStorage.removeItem('user')
      setUser(null)
    } finally {
      setLoading(false)
    }
  }, [])

  const isAdmin = user?.role === 'admin'
  const isAuthenticated = !!user && Object.keys(user).length > 0

  return {
    user,
    loading,
    isAdmin,
    isAuthenticated,
  }
}
