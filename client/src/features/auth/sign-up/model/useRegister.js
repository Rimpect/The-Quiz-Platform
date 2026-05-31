import { useState } from 'react'

import { toast } from 'sonner'

import { registerSchema } from './registerSchema'

export function useRegister() {
  const [loading, setLoading] = useState(false)
  const register = async (formData) => {
    const result = registerSchema.safeParse(formData)

    if (!result.success) {
      toast.error(result.error.issues[0].message)
      return false
    }
    try {
      setLoading(true)
      await new Promise((resolve) => setTimeout(resolve, 1000))
      toast.success('Регистрация успешна')
      return true
    } catch {
      toast.error('Ошибка регистрации')
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
