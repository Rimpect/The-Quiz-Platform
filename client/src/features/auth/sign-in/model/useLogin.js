import { useAuthStore } from '@entities'
import { toast } from 'sonner'

export function useLogin() {
  const login = useAuthStore((state) => state.login)
  const loading = useAuthStore((state) => state.loading)

  const handleLogin = async (formData) => {
    const { success, error } = await login(formData.email, formData.password)

    if (success) {
      toast.success('Добро пожаловать!')
      return true
    } else {
      toast.error(error || 'Ошибка входа')
      return false
    }
  }

  return {
    login: handleLogin,
    loading,
  }
}
