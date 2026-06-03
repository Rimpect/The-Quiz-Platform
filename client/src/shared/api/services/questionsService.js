import { client } from '../client'
import { endpoints } from '../endpoints'

export const questionsService = {
  getQuestionsByQuiz: (quizId) =>
    client(endpoints.questions.byQuiz(quizId), {
      method: 'GET',
    }),

  getQuestionById: (quizId, questionId) =>
    client(endpoints.questions.byId(quizId, questionId), {
      method: 'GET',
    }),
}
