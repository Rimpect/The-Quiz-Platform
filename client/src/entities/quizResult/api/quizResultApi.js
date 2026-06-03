export const createQuizResult = (data) =>
  request('/quiz-results', {
    method: 'POST',
    body: JSON.stringify(data),
  })

export const getMyResults = () => request('/quiz-results/me')

export const getResultById = (id) => request(`/quiz-results/${id}`)

export const saveAnswer = (resultId, answer) =>
  request(`/quiz-results/${resultId}/answer`, {
    method: 'POST',
    body: JSON.stringify(answer),
  })

export const completeQuiz = (resultId) =>
  request(`/quiz-results/${resultId}/complete`, {
    method: 'POST',
  })

export const getQuizLeaderboard = (quizId) =>
  request(`/quiz-results/quiz/${quizId}/leaderboard`)
