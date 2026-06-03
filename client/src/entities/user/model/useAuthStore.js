import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { authService } from '@shared'

export const useAuthStore = create(
  persist(
    (set, get) => ({
      token: null,
      refreshToken: null,
      user: null,
      isLoading: false,
      error: null,
      isAuthenticated: false,

      login: async (email, password) => {
        set({ isLoading: true, error: null })
        try {
          const response = await authService.login({ email, password })
          set({
            token: response.access_token,
            refreshToken: response.refresh_token,
            isAuthenticated: true,
            isLoading: false,
          })
          return response
        } catch (err) {
          set({
            error: err.message || 'Login failed',
            isLoading: false,
          })
          throw err
        }
      },

      logout: async () => {
        set({ isLoading: true })
        try {
          await authService.logout()
          set({
            token: null,
            refreshToken: null,
            user: null,
            isAuthenticated: false,
            isLoading: false,
          })
        } catch (err) {
          set({ error: err.message, isLoading: false })
        }
      },

      logoutAll: async () => {
        set({ isLoading: true })
        try {
          await authService.logoutAll()
          set({
            token: null,
            refreshToken: null,
            user: null,
            isAuthenticated: false,
            isLoading: false,
          })
        } catch (err) {
          set({ error: err.message, isLoading: false })
        }
      },

      refreshAccessToken: async () => {
        try {
          const response = await authService.refresh()
          set({ token: response.access_token })
          return response.access_token
        } catch (err) {
          set({ token: null, isAuthenticated: false })
          throw err
        }
      },

      setUser: (user) => set({ user }),

      setToken: (token) => set({ token }),

      clearError: () => set({ error: null }),
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        token: state.token,
        refreshToken: state.refreshToken,
        user: state.user,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
)
