// shared/hooks/useCurrentUser.js
import { useState, useEffect } from 'react'

export function useCurrentUser() {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const storedUser = localStorage.getItem('user')
    if (storedUser) {
      try {
        setUser(JSON.parse(storedUser))
      } catch (error) {
        console.error('Ошибка парсинга пользователя:', error)
        localStorage.removeItem('user')
      }
    }
    setLoading(false)
  }, [])

  const isAdmin = user?.role === 'admin'
  const isAuthenticated = !!user

  return {
    user,
    loading,
    isAdmin,
    isAuthenticated,
  }
}
