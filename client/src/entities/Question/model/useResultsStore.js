import { create } from 'zustand'
import { resultsService } from '@shared'

export const useResultsStore = create((set) => ({
  results: [],
  currentResult: null,
  leaderboard: [],
  isLoading: false,
  error: null,

  fetchResults: async () => {
    set({ isLoading: true, error: null })
    try {
      const results = await resultsService.getResults()
      set({ results, isLoading: false })
      return results
    } catch (err) {
      set({ error: err.message, isLoading: false })
      throw err
    }
  },

  fetchCurrentUserResults: async () => {
    set({ isLoading: true, error: null })
    try {
      const results = await resultsService.getCurrentUserResults()
      set({ results, isLoading: false })
      return results
    } catch (err) {
      set({ error: err.message, isLoading: false })
      throw err
    }
  },

  fetchResultById: async (resultId) => {
    set({ isLoading: true, error: null })
    try {
      const result = await resultsService.getResultById(resultId)
      set({ currentResult: result, isLoading: false })
      return result
    } catch (err) {
      set({ error: err.message, isLoading: false })
      throw err
    }
  },

  createResult: async (data) => {
    set({ isLoading: true, error: null })
    try {
      const result = await resultsService.createResult(data)
      set({ currentResult: result, isLoading: false })
      return result
    } catch (err) {
      set({ error: err.message, isLoading: false })
      throw err
    }
  },

  submitAnswer: async (resultId, answerData) => {
    set({ isLoading: true, error: null })
    try {
      const result = await resultsService.submitAnswer(resultId, answerData)
      set({ currentResult: result, isLoading: false })
      return result
    } catch (err) {
      set({ error: err.message, isLoading: false })
      throw err
    }
  },

  completeQuiz: async (resultId) => {
    set({ isLoading: true, error: null })
    try {
      const result = await resultsService.completeQuiz(resultId)
      set((state) => ({
        currentResult: result,
        results: state.results.map((r) =>
          r.id === resultId ? result : r
        ),
        isLoading: false,
      }))
      return result
    } catch (err) {
      set({ error: err.message, isLoading: false })
      throw err
    }
  },

  fetchLeaderboard: async (quizId) => {
    set({ isLoading: true, error: null })
    try {
      const leaderboard = await resultsService.getLeaderboard(quizId)
      set({ leaderboard, isLoading: false })
      return leaderboard
    } catch (err) {
      set({ error: err.message, isLoading: false })
      throw err
    }
  },

  setCurrentResult: (result) => set({ currentResult: result }),

  clearError: () => set({ error: null }),
}))
