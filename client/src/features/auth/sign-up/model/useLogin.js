// model/useLogin.js
import { useState } from 'react'
import { toast } from 'sonner'
import { loginSchema } from './loginSchema'

const API_URL = 'http://localhost:3001'

export function useLogin() {
  const [loading, setLoading] = useState(false)

  const login = async (formData) => {
    const result = loginSchema.safeParse(formData)

    if (!result.success) {
      toast.error(result.error.issues[0].message)
      return false
    }

    try {
      setLoading(true)

      // имитация запроса к беку (пока что обращаемся к серверу)
      const response = await fetch(
        `${API_URL}/users?email=${encodeURIComponent(formData.email)}&password=${encodeURIComponent(formData.password)}`,
      )

      if (!response.ok) {
        throw new Error('Ошибка сервера')
      }

      const users = await response.json()

      if (users && users.length > 0) {
        const user = users[0]

        const { password, ...userWithoutPassword } = user
        localStorage.setItem('user', JSON.stringify(userWithoutPassword))

        toast.success(`Добро пожаловать, ${user.name}!`)
        return true
      } else {
        toast.error('Неверный email или пароль')
        return false
      }
    } catch (error) {
      console.error('Login error:', error)
      toast.error('Ошибка соединения с сервером')
      return false
    } finally {
      setLoading(false)
    }
  }

  return {
    login,
    loading,
  }
}
