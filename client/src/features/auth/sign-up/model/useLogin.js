import { useState } from 'react'

import { toast } from 'sonner'

import { loginSchema } from './loginSchema'

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

      // mock api
      await new Promise((resolve) => setTimeout(resolve, 1000))

      // @TODO ВРЕМЕННО: принимаются любые данные

      if (formData.email && formData.password) {
        localStorage.setItem(
          'user',
          JSON.stringify({
            email: formData.email,
            name: formData.email.split('@')[0],
          }),
        )

        toast.success('Успешный вход(ВРЕМЕННО РАБОТАЕТ С ЛЮБЫМИ ДАННЫМИ)')
        return true
      } else {
        toast.error('Заполните все поля')
        return false
      }
    } catch {
      toast.error('Неверный email или пароль')
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
