import { create } from 'zustand'
import { quizzesService } from '@shared'

export const useQuizzesStore = create((set) => ({
  quizzes: [],
  currentQuiz: null,
  categories: [],
  isLoading: false,
  error: null,

  fetchQuizzes: async () => {
    set({ isLoading: true, error: null })
    try {
      const quizzes = await quizzesService.getQuizzes()
      set({ quizzes, isLoading: false })
      return quizzes
    } catch (err) {
      set({ error: err.message, isLoading: false })
      throw err
    }
  },

  fetchQuizById: async (quizId) => {
    set({ isLoading: true, error: null })
    try {
      const quiz = await quizzesService.getQuizById(quizId)
      set({ currentQuiz: quiz, isLoading: false })
      return quiz
    } catch (err) {
      set({ error: err.message, isLoading: false })
      throw err
    }
  },

  fetchQuizFull: async (quizId) => {
    set({ isLoading: true, error: null })
    try {
      const quiz = await quizzesService.getQuizFull(quizId)
      set({ currentQuiz: quiz, isLoading: false })
      return quiz
    } catch (err) {
      set({ error: err.message, isLoading: false })
      throw err
    }
  },

  createQuiz: async (data) => {
    set({ isLoading: true, error: null })
    try {
      const quiz = await quizzesService.createQuiz(data)
      set({ isLoading: false })
      return quiz
    } catch (err) {
      set({ error: err.message, isLoading: false })
      throw err
    }
  },

  updateQuiz: async (quizId, data) => {
    set({ isLoading: true, error: null })
    try {
      const quiz = await quizzesService.updateQuiz(quizId, data)
      set({ currentQuiz: quiz, isLoading: false })
      return quiz
    } catch (err) {
      set({ error: err.message, isLoading: false })
      throw err
    }
  },

  deleteQuiz: async (quizId) => {
    set({ isLoading: true, error: null })
    try {
      await quizzesService.deleteQuiz(quizId)
      set((state) => ({
        quizzes: state.quizzes.filter((q) => q.id !== quizId),
        currentQuiz: state.currentQuiz?.id === quizId ? null : state.currentQuiz,
        isLoading: false,
      }))
    } catch (err) {
      set({ error: err.message, isLoading: false })
      throw err
    }
  },

  fetchCategories: async () => {
    set({ isLoading: true, error: null })
    try {
      const categories = await quizzesService.getCategories()
      set({ categories, isLoading: false })
      return categories
    } catch (err) {
      set({ error: err.message, isLoading: false })
      throw err
    }
  },

  fetchLeaderboard: async (quizId) => {
    set({ isLoading: true, error: null })
    try {
      const leaderboard = await quizzesService.getLeaderboard(quizId)
      return leaderboard
    } catch (err) {
      set({ error: err.message, isLoading: false })
      throw err
    }
  },

  setCurrentQuiz: (quiz) => set({ currentQuiz: quiz }),

  clearError: () => set({ error: null }),
}))
