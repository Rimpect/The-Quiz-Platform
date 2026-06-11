import { useState } from 'react'

import { useAuthStore } from '@entities'
import { registerUser } from '@entities/user/api/authApi.js'
import { toast } from 'sonner'

import { registerSchema } from './registerSchema'

export function useRegister() {
  const [loading, setLoading] = useState(false)
  const login = useAuthStore((state) => state.login)

  const register = async (formData) => {
    const result = registerSchema.safeParse(formData)

    if (!result.success) {
      toast.error(result.error.issues[0].message)
      return false
    }

    try {
      setLoading(true)
      await registerUser({
        name: formData.name,
        email: formData.email,
        password: formData.password,
      })

      const loginResult = await login(formData.email, formData.password)
      if (!loginResult.success) {
        toast.error(loginResult.error || 'Не удалось войти после регистрации')
        return false
      }

      toast.success('Регистрация успешна')
      return true
    } catch (error) {
      toast.error(error?.message || 'Ошибка регистрации')
      return false
    } finally {
      setLoading(false)
    }
  }
  return {
    register,
    loading,
  }
}
