import { create } from 'zustand'

import { getQuestions } from '../api/QuestionApi/QuestionApi.js'

import { questionSchema } from './questionSchema.js'

const inferMediaType = (url) => {
  if (!url) return null
  if (url.includes('/quest_audio/')) return 'audio'
  if (url.includes('/quest_video/')) return 'video'
  if (url.includes('/quest_image/')) return 'image'
  if (/\.(mp3|wav|ogg|m4a|aac)$/i.test(url)) return 'audio'
  if (/\.(mp4|mov|mkv|avi)$/i.test(url)) return 'video'
  return 'image'
}

const mapQuestion = (q) => {
  const answers = q.answers || []
  return {
    id: String(q.id),
    quizId: q.quiz_id,
    question: q.question_text,
    questionType: q.answer_type === 'multiple' ? 'multiple' : 'single',
    options: answers.map((a) => a.answer_text),
    correctAnswers: answers
      .map((a, idx) => (a.is_correct ? idx : null))
      .filter((idx) => idx !== null),
    points: q.points,
    mediaUrl: q.media_url ?? null,
    mediaType: inferMediaType(q.media_url),
    timeLimitSeconds: q.time_limit_seconds ?? null,
  }
}

const initialState = {
  questions: [],
  loading: false,
  error: null,
}

export const useQuestionStore = create((set) => ({
  ...initialState,
  fetchQuestions: async (quizId) => {
    set({ loading: true, error: null })
    try {
      const raw = await getQuestions(quizId)
      const mapped = (Array.isArray(raw) ? raw : []).map(mapQuestion)
      const validated = questionSchema.parse(mapped)
      set({ questions: validated, loading: false })
    } catch (error) {
      console.error('Ошибка при загрузке вопросов:', error)
      set({ error: error.message, loading: false })
    }
  },
}))

export const useQuestions = () => useQuestionStore((state) => state.questions)
