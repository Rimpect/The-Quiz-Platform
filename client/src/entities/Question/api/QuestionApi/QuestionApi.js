import { client } from '@shared/api/client'

export const getQuestions = (quizId) => client(`/quizzes/${quizId}/questions`)
