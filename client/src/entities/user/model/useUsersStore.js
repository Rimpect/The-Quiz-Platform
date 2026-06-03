import { usersService } from '@shared'
import { create } from 'zustand'

export const useUsersStore = create((set) => ({
  currentUser: null,
  users: [],
  isLoading: false,
  error: null,

  fetchCurrentUser: async () => {
    set({ isLoading: true, error: null })
    try {
      const user = await usersService.getCurrentUser()
      set({ currentUser: user, isLoading: false })
      return user
    } catch (err) {
      set({ error: err.message, isLoading: false })
      throw err
    }
  },

  fetchUserById: async (userId) => {
    set({ isLoading: true, error: null })
    try {
      const user = await usersService.getUserById(userId)
      return user
    } catch (err) {
      set({ error: err.message, isLoading: false })
      throw err
    }
  },

  fetchUsers: async () => {
    set({ isLoading: true, error: null })
    try {
      const users = await usersService.getUsers()
      set({ users, isLoading: false })
      return users
    } catch (err) {
      set({ error: err.message, isLoading: false })
      throw err
    }
  },

  updateCurrentUser: async (data) => {
    set({ isLoading: true, error: null })
    try {
      const user = await usersService.updateCurrentUser(data)
      set({ currentUser: user, isLoading: false })
      return user
    } catch (err) {
      set({ error: err.message, isLoading: false })
      throw err
    }
  },

  deleteCurrentUser: async () => {
    set({ isLoading: true, error: null })
    try {
      await usersService.deleteCurrentUser()
      set({ currentUser: null, isLoading: false })
    } catch (err) {
      set({ error: err.message, isLoading: false })
      throw err
    }
  },

  fetchStatistics: async () => {
    set({ isLoading: true, error: null })
    try {
      const stats = await usersService.getStatistics()
      return stats
    } catch (err) {
      set({ error: err.message, isLoading: false })
      throw err
    }
  },

  setCurrentUser: (user) => set({ currentUser: user }),

  clearError: () => set({ error: null }),
}))
