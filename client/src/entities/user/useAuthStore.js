import { loginSchema } from '@features'
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

import { loginUser } from './api/authApi.js'
import { validateUser } from './userSchema'

const initialState = {
  user: null,
  loading: false,
  isAuthenticated: false,
  error: null,
}

export const useAuthStore = create(
  persist(
    (set) => ({
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
          const users = await loginUser({ email, password })

          if (users && users.length > 0) {
            const { password, ...userData } = users[0]
            void password

            const normalizedUser = {
              ...userData,
              id:
                typeof userData.id === 'string' && /^\d+$/.test(userData.id)
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

export const useUser = () => useAuthStore((state) => state.user)
export const useIsAuthenticated = () =>
  useAuthStore((state) => state.isAuthenticated)
export const useIsAdmin = () =>
  useAuthStore((state) => state.user?.role === 'admin')
export const useAuthLoading = () => useAuthStore((state) => state.loading)
export const useAuthError = () => useAuthStore((state) => state.error)
