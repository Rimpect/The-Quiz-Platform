import { authService, IS_DEMO } from '@shared'
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

// В демо-режиме пользователь «залогинен» сразу как демо-админ.
const DEMO_USER = {
  id: 1,
  nickname: 'Демо-пользователь',
  role: 'admin',
  photo_profile: null,
}

export const useAuthStore = create(
  persist(
    (set) => ({
      token: IS_DEMO ? 'demo-token' : null,
      refreshToken: null,
      user: IS_DEMO ? DEMO_USER : null,
      isLoading: false,
      error: null,
      isAuthenticated: IS_DEMO,

      login: async (email, password) => {
        set({ isLoading: true, error: null })
        try {
          const response = await authService.login({ email, password })
          const data = response?.data ?? response
          set({
            token: data.access_token,
            user: {
              id: data.user_id,
              nickname: data.nickname,
              role: data.role,
              photo_profile: data.photo_profile || null,
            },
            isAuthenticated: true,
            isLoading: false,
          })
          return { success: true }
        } catch (err) {
          const message = err.message || 'Ошибка входа'
          set({ error: message, isLoading: false })
          return { success: false, error: message }
        }
      },

      logout: async () => {
        set({ isLoading: true })
        try {
          await authService.logout()
        } catch (_) {
          // ignore logout errors
        } finally {
          set({
            token: null,
            refreshToken: null,
            user: null,
            isAuthenticated: false,
            isLoading: false,
          })
        }
      },

      logoutAll: async () => {
        set({ isLoading: true })
        try {
          await authService.logoutAll()
        } catch (_) {
          // ignore
        } finally {
          set({
            token: null,
            refreshToken: null,
            user: null,
            isAuthenticated: false,
            isLoading: false,
          })
        }
      },

      refreshAccessToken: async () => {
        try {
          const response = await authService.refresh()
          const data = response?.data ?? response
          set({ token: data.access_token })
          return data.access_token
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
    },
  ),
)

if (typeof window !== 'undefined') {
  window.addEventListener('auth:refreshed', (e) => {
    if (e.detail) useAuthStore.getState().setToken(e.detail)
  })
}

export const useUser = () => useAuthStore((state) => state.user)
export const useIsAuthenticated = () =>
  useAuthStore((state) => state.isAuthenticated)
export const useIsAdmin = () =>
  useAuthStore((state) => state.user?.role === 'admin')
export const useAuthLoading = () => useAuthStore((state) => state.isLoading)
export const useAuthError = () => useAuthStore((state) => state.error)
