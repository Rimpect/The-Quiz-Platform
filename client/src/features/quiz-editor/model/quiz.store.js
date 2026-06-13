import { create } from 'zustand'

const createQuestion = () => ({
  id: Date.now(),
  questionText: '',
  questionType: 'single',
  timeLimitSeconds: 0,
  points: 10,
  mediaUrl: '',
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
  editQuizId: null,
  quiz: {
    title: '',
    description: '',
    categoryId: '',
    difficulty: '',
    quizMode: 'single',
    duration: 10,
    lobbyWaitTimeSeconds: 30,
    maxTeamMembers: 10,
    coverUrl: '',

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

  toggleCorrectAnswer: (questionId, answerId) =>
    set((state) => ({
      quiz: {
        ...state.quiz,
        questions: state.quiz.questions.map((q) => {
          if (q.id !== questionId) return q
          return {
            ...q,
            answers: q.answers.map((a) =>
              a.id === answerId ? { ...a, isCorrect: !a.isCorrect } : a,
            ),
          }
        }),
      },
    })),

  setQuestionType: (questionId, type) =>
    set((state) => ({
      quiz: {
        ...state.quiz,
        questions: state.quiz.questions.map((q) => {
          if (q.id !== questionId) return q

          let answers = q.answers
          if (type === 'single') {
            let kept = false
            answers = q.answers.map((a) => {
              if (a.isCorrect && !kept) {
                kept = true
                return a
              }
              return { ...a, isCorrect: false }
            })
          }
          return { ...q, questionType: type, answers }
        }),
      },
    })),

  loadQuiz: (data) =>
    set({
      editQuizId: data.id || null,
      quiz: {
        title: data.title || '',
        description: data.description || '',
        categoryId: data.categoryId || '',
        difficulty: data.difficulty || '',
        quizMode: data.quizMode || 'single',
        duration: 10,
        lobbyWaitTimeSeconds: data.lobbyWaitTimeSeconds || 30,
        maxTeamMembers: data.maxTeamMembers || 10,
        coverUrl: data.coverUrl || '',
        questions: (data.questions || []).map((q) => ({
          id: q.id || Date.now() + Math.random(),
          questionText: q.questionText || '',
          questionType: q.questionType || 'single',
          timeLimitSeconds: q.timeLimitSeconds || 0,
          points: q.points || 10,
          mediaUrl: q.mediaUrl || '',
          answers: (q.answers || []).map((a) => ({
            id: a.id || Math.random(),
            text: a.text || '',
            isCorrect: a.isCorrect || false,
          })),
        })),
      },
    }),

  resetQuiz: () =>
    set({
      editQuizId: null,
      quiz: {
        title: '',
        description: '',
        categoryId: '',
        difficulty: '',
        quizMode: 'single',
        duration: 10,
        lobbyWaitTimeSeconds: 30,
        maxTeamMembers: 10,
        coverUrl: '',
        questions: [createQuestion()],
      },
    }),
}))
