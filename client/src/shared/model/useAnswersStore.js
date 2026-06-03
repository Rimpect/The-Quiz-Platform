import { answersService } from '@shared'
import { create } from 'zustand'

export const useAnswersStore = create((set) => ({
  answers: [],
  currentAnswer: null,
  isLoading: false,
  error: null,

  fetchAnswersByQuestion: async (questionId) => {
    set({ isLoading: true, error: null })
    try {
      const answers = await answersService.getAnswersByQuestion(questionId)
      set({ answers, isLoading: false })
      return answers
    } catch (err) {
      set({ error: err.message, isLoading: false })
      throw err
    }
  },

  fetchAnswerById: async (questionId, answerId) => {
    set({ isLoading: true, error: null })
    try {
      const answer = await answersService.getAnswerById(questionId, answerId)
      set({ currentAnswer: answer, isLoading: false })
      return answer
    } catch (err) {
      set({ error: err.message, isLoading: false })
      throw err
    }
  },

  updateAnswer: async (questionId, answerId, data) => {
    set({ isLoading: true, error: null })
    try {
      const answer = await answersService.updateAnswer(
        questionId,
        answerId,
        data,
      )
      set((state) => ({
        answers: state.answers.map((a) => (a.id === answerId ? answer : a)),
        currentAnswer: answer,
        isLoading: false,
      }))
      return answer
    } catch (err) {
      set({ error: err.message, isLoading: false })
      throw err
    }
  },

  deleteAnswer: async (questionId, answerId) => {
    set({ isLoading: true, error: null })
    try {
      await answersService.deleteAnswer(questionId, answerId)
      set((state) => ({
        answers: state.answers.filter((a) => a.id !== answerId),
        currentAnswer:
          state.currentAnswer?.id === answerId ? null : state.currentAnswer,
        isLoading: false,
      }))
    } catch (err) {
      set({ error: err.message, isLoading: false })
      throw err
    }
  },

  setCurrentAnswer: (answer) => set({ currentAnswer: answer }),

  clearError: () => set({ error: null }),
}))
