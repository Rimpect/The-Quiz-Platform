import { client } from '@shared/api/client'

import { quizSchema } from '../../quiz-editor/model/quiz.schema'

const toServerFormat = (quiz) => ({
  title: quiz.title,
  description: quiz.description || ' ',
  category_id:
    quiz.categoryId && quiz.categoryId !== 'other'
      ? Number(quiz.categoryId)
      : null,
  category_name:
    quiz.categoryId === 'other' && quiz.categoryName?.trim()
      ? quiz.categoryName.trim()
      : null,
  is_public: true,
  quiz_mode: quiz.quizMode || 'single',
  difficulty: quiz.difficulty || 'easy',
  lobby_wait_time_seconds: quiz.lobbyWaitTimeSeconds || 30,
  max_team_members: quiz.maxTeamMembers || 10,
  cover_url: quiz.coverUrl || null,
  questions: quiz.questions.map((q) => ({
    question_text: q.questionText,
    answer_type: q.questionType === 'multiple' ? 'multiple' : 'single',
    points: q.points || 10,
    media_url: q.mediaUrl || null,
    time_limit_seconds:
      q.timeLimitSeconds && q.timeLimitSeconds >= 5 ? q.timeLimitSeconds : null,
    answers: q.answers.map((a, idx) => ({
      answer_text: a.text,
      is_correct: a.isCorrect,
      order_number: idx + 1,
    })),
  })),
})

export const saveQuiz = async (quizData, editQuizId = null) => {
  const result = quizSchema.safeParse(quizData)
  if (!result.success) {
    throw new Error(result.error.issues[0].message)
  }

  const serverData = toServerFormat(quizData)

  if (editQuizId) {
    return client(`/quizzes/${editQuizId}/bulk`, {
      method: 'PUT',
      body: JSON.stringify(serverData),
    })
  }

  return client('/quizzes/bulk', {
    method: 'POST',
    body: JSON.stringify(serverData),
  })
}
