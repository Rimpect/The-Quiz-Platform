import { create } from 'zustand'

import { getQuestions } from '../api/QuestionApi/QuestionApi.js'

import { questionSchema } from './questionSchema.js'

const initialState = {
  questions: [],
  loading: false,
  error: null,
}

export const useQuestionStore = create(
  (set) => ({
    ...initialState,
    fetchQuestions: async (quizId) => {
      set({ loading: true, error: null })

      try {
        const data = await getQuestions(quizId)
        console.log('Raw data:', data)

        const validatedQuestions = questionSchema.parse(data)
        console.log('Валидированные вопросы:', validatedQuestions)

        set({
          questions: validatedQuestions,
          loading: false,
        })
      } catch (error) {
        console.error('Ошибка при загрузке вопросов:', error)
        set({
          error: error.message,
          loading: false,
        })
      }
    },
  }),
  { name: 'questions' },
)
export const useQuestions = () => useQuestionStore((state) => state.questions)
