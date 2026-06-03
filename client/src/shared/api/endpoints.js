export const endpoints = {
  auth: {
    login: '/auth/login',
    logout: '/auth/logout',
    refresh: '/auth/refresh',
    sessions: '/auth/sessions',
    history: '/auth/history',
  },

  users: {
    base: '/users',
    me: '/users/me',
    statistics: '/users/me/statistics',
  },

  quizzes: {
    base: '/quizzes',
    categories: '/quizzes/categories',
    full: (id) => `/quizzes/${id}/full`,
    byId: (id) => `/quizzes/${id}`,
    leaderboard: (id) => `/quizzes/${id}/leaderboard`,
  },

  questions: {
    byQuiz: (quizId) => `/quizzes/${quizId}/questions`,
    byId: (quizId, questionId) => `/quizzes/${quizId}/questions/${questionId}`,
  },

  answers: {
    byQuestion: (questionId) => `/questions/${questionId}/answers`,
  },

  media: {
    upload: (type, id) => `/media/upload/${type}/${id}`,
    uploadMultiple: (type, id) => `/media/upload-multiple/${type}/${id}`,
    entity: (type, id) => `/media/entity/${type}/${id}`,
  },

  results: {
    base: '/quiz-results',
    me: '/quiz-results/me',
    byId: (id) => `/quiz-results/${id}`,
    answer: (id) => `/quiz-results/${id}/answer`,
    complete: (id) => `/quiz-results/${id}/complete`,
    leaderboard: (quizId) => `/quiz-results/quiz/${quizId}/leaderboard`,
  },
}
