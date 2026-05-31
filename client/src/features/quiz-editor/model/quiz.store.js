import { create } from 'zustand'

const createQuestion = () => ({
  id: Date.now(),

  questionText: '',

  answers: [
    {
      id: 1,
      text: '',
      isCorrect: false,
    },
    {
      id: 2,
      text: '',
      isCorrect: false,
    },
  ],
})

export const useQuizStore = create((set) => ({
  quiz: {
    title: '',
    description: '',
    category: '',
    difficulty: '',
    duration: 10,

    questions: [createQuestion()],
  },

  setField: (field, value) =>
    set((state) => ({
      quiz: {
        ...state.quiz,
        [field]: value,
      },
    })),

  addQuestion: () =>
    set((state) => ({
      quiz: {
        ...state.quiz,
        questions: [...state.quiz.questions, createQuestion()],
      },
    })),

  deleteQuestion: (questionId) =>
    set((state) => ({
      quiz: {
        ...state.quiz,
        questions: state.quiz.questions.filter((q) => q.id !== questionId),
      },
    })),

  updateQuestion: (id, field, value) =>
    set((state) => ({
      quiz: {
        ...state.quiz,
        questions: state.quiz.questions.map((q) =>
          q.id === id
            ? {
                ...q,
                [field]: value,
              }
            : q,
        ),
      },
    })),

  addAnswer: (questionId) =>
    set((state) => ({
      quiz: {
        ...state.quiz,
        questions: state.quiz.questions.map((q) => {
          if (q.id !== questionId) return q

          const newId = Math.max(...q.answers.map((a) => a.id)) + 1

          return {
            ...q,
            answers: [
              ...q.answers,
              {
                id: newId,
                text: '',
                isCorrect: false,
              },
            ],
          }
        }),
      },
    })),

  removeAnswer: (questionId, answerId) =>
    set((state) => ({
      quiz: {
        ...state.quiz,
        questions: state.quiz.questions.map((q) => {
          if (q.id !== questionId) return q

          return {
            ...q,
            answers: q.answers.filter((a) => a.id !== answerId),
          }
        }),
      },
    })),

  updateAnswerText: (questionId, answerId, text) =>
    set((state) => ({
      quiz: {
        ...state.quiz,
        questions: state.quiz.questions.map((q) => {
          if (q.id !== questionId) return q

          return {
            ...q,
            answers: q.answers.map((a) =>
              a.id === answerId
                ? {
                    ...a,
                    text,
                  }
                : a,
            ),
          }
        }),
      },
    })),

  setCorrectAnswer: (questionId, answerId) =>
    set((state) => ({
      quiz: {
        ...state.quiz,
        questions: state.quiz.questions.map((q) => {
          if (q.id !== questionId) return q

          return {
            ...q,
            answers: q.answers.map((a) => ({
              ...a,
              isCorrect: a.id === answerId,
            })),
          }
        }),
      },
    })),
}))
