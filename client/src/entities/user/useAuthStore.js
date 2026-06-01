import { registerSchema, loginSchema } from '@features'
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

import { validateUser } from './userSchema'

const API_URL = 'http://localhost:3001'

const initialState = {
  user: null,
  loading: false,
  isAuthenticated: false,
  error: null,
}

export const useAuthStore = create(
  persist(
    (set, get) => ({
      ...initialState,

      login: async (email, password) => {
        const validation = loginSchema.safeParse({ email, password })
        if (!validation.success) {
          const errorMessage = validation.error.issues[0].message
          set({ error: errorMessage })
          return { success: false, error: errorMessage }
        }

        set({ loading: true, error: null })

        try {
          const response = await fetch(
            `${API_URL}/users?email=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`,
          )

          if (!response.ok) {
            throw new Error('Ошибка сервера')
          }

          const users = await response.json()

          if (users && users.length > 0) {
            const { password: _, ...userData } = users[0]

            const normalizedUser = {
              ...userData,
              id:
                typeof userData.id === 'string'
                  ? parseInt(userData.id, 10)
                  : userData.id,
            }

            const userValidation = validateUser(normalizedUser)
            if (!userValidation.isValid) {
              throw new Error(userValidation.error)
            }

            set({
              user: userValidation.data,
              isAuthenticated: true,
              loading: false,
              error: null,
            })
            console.log('User saved:', userValidation.data)
            console.log('Is authenticated:', true)

            return { success: true, user: userValidation.data }
          } else {
            set({ loading: false, error: 'Неверный email или пароль' })
            return { success: false, error: 'Неверный email или пароль' }
          }
        } catch (error) {
          console.error('Login error:', error)
          set({ loading: false, error: error.message })
          return { success: false, error: error.message }
        }
      },

      logout: () => {
        set(initialState)
      },

      clearError: () => {
        set({ error: null })
      },
    }),
    {
      name: 'auth-storage',
      getStorage: () => localStorage,
      partialize: (state) => ({
        user: state.user,
        isAuthenticated: state.isAuthenticated,
      }),
    },
  ),
)

export const useUser = () => {
  const user = useAuthStore((state) => state.user)
  console.log('useUser hook:', user)
  return user
}
export const useIsAuthenticated = () =>
  useAuthStore((state) => state.isAuthenticated)
export const useIsAdmin = () => {
  const isAdmin = useAuthStore((state) => state.user?.role === 'admin')
  console.log('useIsAdmin hook:', isAdmin)
  return isAdmin
}
export const useAuthLoading = () => useAuthStore((state) => state.loading)
export const useAuthError = () => useAuthStore((state) => state.error)
