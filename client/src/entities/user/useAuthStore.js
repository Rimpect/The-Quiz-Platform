import { loginSchema } from '@features'
import { authService } from '@shared'
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

const initialState = {
  token: null,
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
          const response = await authService.login({ email, password })
          // Server wraps response in { data: { access_token, user_id, nickname, role } }
          const data = response?.data ?? response

          const user = {
            id: data.user_id,
            name: data.nickname,
            nickname: data.nickname,
            role: data.role,
          }

          set({
            token: data.access_token,
            user,
            isAuthenticated: true,
            loading: false,
            error: null,
          })

          return { success: true, user }
        } catch (error) {
          const message = error.message || 'Неверный email или пароль'
          set({ loading: false, error: message })
          return { success: false, error: message }
        }
      },

      logout: async () => {
        try {
          await authService.logout()
        } catch {
          // ignore server errors on logout
        } finally {
          set(initialState)
        }
      },

      clearError: () => {
        set({ error: null })
      },
    }),
    {
      name: 'auth-storage',
      getStorage: () => localStorage,
      partialize: (state) => ({
        token: state.token,
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
