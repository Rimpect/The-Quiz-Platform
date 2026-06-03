export const getQuestions = (quizId) => request(`/quizzes/${quizId}/questions`)

export const getQuestionById = (quizId, questionId) =>
  request(`/quizzes/${quizId}/questions/${questionId}`)
