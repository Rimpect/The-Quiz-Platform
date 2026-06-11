import { client } from '../client'
import { endpoints } from '../endpoints'

export const resultsService = {
  createResult: (data) =>
    client(endpoints.results.base, {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  getResults: () =>
    client(endpoints.results.base, {
      method: 'GET',
    }),

  getResultById: (resultId) =>
    client(endpoints.results.byId(resultId), {
      method: 'GET',
    }),

  getCurrentUserResults: () =>
    client(endpoints.results.me, {
      method: 'GET',
    }),

  submitAnswer: (resultId, answerData) =>
    client(endpoints.results.answer(resultId), {
      method: 'POST',
      body: JSON.stringify(answerData),
    }),

  completeQuiz: (resultId) =>
    client(endpoints.results.complete(resultId), {
      method: 'POST',
    }),

  getLeaderboard: (quizId) =>
    client(endpoints.results.leaderboard(quizId), {
      method: 'GET',
    }),
}
