import { client } from '../client'
import { endpoints } from '../endpoints'

export const quizzesService = {
  createQuiz: (data) =>
    client(endpoints.quizzes.base, {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  createQuizBulk: (data) =>
    client(endpoints.quizzes.bulk, {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  getQuizzes: () =>
    client(endpoints.quizzes.base, {
      method: 'GET',
    }),

  getQuizById: (quizId) =>
    client(endpoints.quizzes.byId(quizId), {
      method: 'GET',
    }),

  getQuizFull: (quizId) =>
    client(endpoints.quizzes.full(quizId), {
      method: 'GET',
    }),

  updateQuiz: (quizId, data) =>
    client(endpoints.quizzes.byId(quizId), {
      method: 'PUT',
      body: JSON.stringify(data),
    }),

  deleteQuiz: (quizId) =>
    client(endpoints.quizzes.byId(quizId), {
      method: 'DELETE',
    }),

  getCategories: () =>
    client(endpoints.quizzes.categories, {
      method: 'GET',
    }),

  getLeaderboard: (quizId) =>
    client(endpoints.quizzes.leaderboard(quizId), {
      method: 'GET',
    }),
}
