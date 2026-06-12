export const endpoints = {
  auth: {
    login: '/auth/login',
    logout: '/auth/logout',
    logoutAll: '/auth/logout-all',
    refresh: '/auth/refresh',
    revokeAccess: '/auth/revoke-access',
    sessions: '/auth/sessions',
    history: '/auth/history',
  },

  users: {
    base: '/users',
    byId: (id) => `/users/${id}`,
    me: '/users/me',
    statistics: '/users/me/statistics',
  },

  quizzes: {
    base: '/quizzes',
    bulk: '/quizzes/bulk',
    categories: '/quizzes/categories',
    full: (id) => `/quizzes/${id}/full`,
    byId: (id) => `/quizzes/${id}`,
    leaderboard: (id) => `/quizzes/${id}/leaderboard`,
  },

  categories: {
    base: '/categories',
  },

  questions: {
    byQuiz: (quizId) => `/quizzes/${quizId}/questions`,
    byId: (quizId, questionId) => `/quizzes/${quizId}/questions/${questionId}`,
  },

  answers: {
    byQuestion: (questionId) => `/questions/${questionId}/answers`,
    byId: (questionId, answerId) =>
      `/questions/${questionId}/answers/${answerId}`,
  },

  media: {
    upload: (type, id) => `/media/upload/${type}/${id}`,
    uploadMultiple: (type, id) => `/media/upload-multiple/${type}/${id}`,
    byPath: (path) => `/media/${path}`,
    entity: (type, id) => `/media/entity/${type}/${id}`,
    update: (id) => `/media/${id}`,
    delete: (id) => `/media/${id}`,
    deleteEntity: (type, id) => `/media/entity/${type}/${id}`,
  },

  achievements: {
    base: '/achievements',
    unlock: (id) => `/achievements/${id}/unlock`,
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
