import { client } from '../client'
import { endpoints } from '../endpoints'

export const answersService = {
  getAnswersByQuestion: (questionId) =>
    client(endpoints.answers.byQuestion(questionId), {
      method: 'GET',
    }),

  getAnswerById: (questionId, answerId) =>
    client(endpoints.answers.byId(questionId, answerId), {
      method: 'GET',
    }),

  updateAnswer: (questionId, answerId, data) =>
    client(endpoints.answers.byId(questionId, answerId), {
      method: 'PUT',
      body: JSON.stringify(data),
    }),

  deleteAnswer: (questionId, answerId) =>
    client(endpoints.answers.byId(questionId, answerId), {
      method: 'DELETE',
    }),
}
