export const getAnswers = (questionId) =>
  request(`/questions/${questionId}/answers`)

export const getAnswerById = (questionId, answerId) =>
  request(`/questions/${questionId}/answers/${answerId}`)

export const updateAnswer = (questionId, answerId, data) =>
  request(`/questions/${questionId}/answers/${answerId}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  })

export const deleteAnswer = (questionId, answerId) =>
  request(`/questions/${questionId}/answers/${answerId}`, {
    method: 'DELETE',
  })
