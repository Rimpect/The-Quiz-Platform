// Демо-«база данных» на localStorage.
// Делает демо-режим похожим на продакшен: сыгранные результаты и созданные
// пользователем квизы сохраняются, а история, статистика, «лучший результат»
// и лидерборд вычисляются из них — как это делал бы реальный бэкенд.

import {
  DEMO_QUIZZES,
  DEMO_CATEGORIES,
  DEMO_LEADERBOARD,
} from './fixtures/quizzes'

const RESULTS_KEY = 'demo:results'
const QUIZZES_KEY = 'demo:quizzes' // созданные пользователем квизы

const read = (key, fallback) => {
  try {
    const raw = localStorage.getItem(key)
    return raw ? JSON.parse(raw) : fallback
  } catch {
    return fallback
  }
}

const write = (key, value) => {
  try {
    localStorage.setItem(key, JSON.stringify(value))
  } catch {
    /* ignore */
  }
}

const parseBody = (body) => {
  try {
    return typeof body === 'string' ? JSON.parse(body || '{}') : body || {}
  } catch {
    return {}
  }
}

const nowISO = () => new Date().toISOString()

// --- Квизы (фикстуры + созданные) ---

const createdQuizzes = () => read(QUIZZES_KEY, [])

const allQuizzes = () => [...createdQuizzes(), ...DEMO_QUIZZES]

const stripQuestions = (quiz) => {
  const copy = { ...quiz }
  delete copy.questions
  return copy
}

const findQuiz = (id) => allQuizzes().find((q) => q.id === Number(id)) || null

const categoryNameById = (id) =>
  DEMO_CATEGORIES.find((c) => c.id === Number(id))?.category_type || null

// Преобразует payload из редактора квизов (toServerFormat) в наш формат квиза.
const fromBulkPayload = (payload, id) => {
  const quizId = id ? Number(id) : Date.now()
  const category =
    payload.category_name ||
    categoryNameById(payload.category_id) ||
    'Мои квизы'

  return {
    id: quizId,
    title: payload.title || 'Без названия',
    description: payload.description || '',
    cover_url: payload.cover_url || null,
    category_obj: { category_type: category },
    difficulty: payload.difficulty || 'easy',
    quiz_mode: payload.quiz_mode || 'single',
    times_taken: 0,
    duration_minutes: 0,
    total_questions: (payload.questions || []).length,
    media_types: [],
    author_name: 'Демо-пользователь',
    created_at: nowISO(),
    status: 'approved',
    questions: (payload.questions || []).map((q, qi) => ({
      id: quizId * 1000 + qi + 1,
      quiz_id: quizId,
      question_text: q.question_text || '',
      answer_type: q.answer_type === 'multiple' ? 'multiple' : 'single',
      points: q.points || 10,
      media_url: q.media_url || null,
      time_limit_seconds: q.time_limit_seconds ?? null,
      answers: (q.answers || []).map((a) => ({
        answer_text: a.answer_text || '',
        is_correct: !!a.is_correct,
      })),
    })),
  }
}

const saveBulk = (body, id) => {
  const quiz = fromBulkPayload(parseBody(body), id)
  const list = createdQuizzes()
  const idx = list.findIndex((q) => q.id === quiz.id)
  if (idx >= 0) list[idx] = quiz
  else list.unshift(quiz)
  write(QUIZZES_KEY, list)
  return quiz
}

const deleteQuiz = (id) => {
  write(
    QUIZZES_KEY,
    createdQuizzes().filter((q) => q.id !== Number(id)),
  )
  return { success: true }
}

// «Мои квизы»: бэкенд отдаёт { approved, pending, rejected }
const myQuizzes = () => ({
  approved: createdQuizzes(),
  pending: [],
  rejected: [],
})

// --- Результаты ---

const results = () => read(RESULTS_KEY, [])

const addResult = (body) => {
  const p = parseBody(body)
  const quiz = findQuiz(p.quiz_id)
  const maxScore = p.max_score || 0
  const percentage = maxScore
    ? Math.round(((p.score || 0) / maxScore) * 100)
    : 0
  const totalQuestions = quiz?.questions?.length ?? quiz?.total_questions ?? 0
  const correct = Math.round((percentage / 100) * totalQuestions)

  const record = {
    id: Date.now(),
    quiz_id: Number(p.quiz_id),
    title: quiz?.title || 'Квиз',
    category: quiz?.category_obj?.category_type || '',
    score: p.score || 0,
    max_score: maxScore,
    percentage,
    correct_answers: correct,
    total_questions: totalQuestions,
    duration_seconds: p.duration_seconds || 0,
    completed_at: nowISO(),
  }

  const list = results()
  list.unshift(record)
  write(RESULTS_KEY, list)
  return record
}

// История в форме, которую ждёт useQuizHistory (r.score = число правильных)
const history = () =>
  results().map((r) => ({
    id: r.id,
    title: r.title,
    category: r.category,
    percentage: r.percentage,
    score: r.correct_answers,
    total_questions: r.total_questions,
    duration_seconds: r.duration_seconds,
    completed_at: r.completed_at,
  }))

const statistics = () => {
  const rs = results()
  const total = rs.length
  const sumPct = rs.reduce((s, r) => s + (r.percentage || 0), 0)
  const sumSec = rs.reduce((s, r) => s + (r.duration_seconds || 0), 0)
  return {
    total_quizzes_completed: total,
    average_score: total ? Math.round(sumPct / total) : 0,
    best_result: total ? Math.max(...rs.map((r) => r.percentage || 0)) : 0,
    total_minutes: Math.round(sumSec / 60),
  }
}

// Лидерборд квиза: базовые «игроки» + лучший результат пользователя по этому квизу
const leaderboardForQuiz = (quizId) => {
  const mine = results()
    .filter((r) => r.quiz_id === Number(quizId))
    .map((r) => r.percentage)
  const board = [...DEMO_LEADERBOARD]
  if (mine.length) {
    const best = Math.max(...mine)
    board.push({
      name: 'Демо-пользователь',
      score: best,
      percent: best,
      time: '—',
      isCurrentUser: true,
    })
  }
  return board.sort((a, b) => b.percent - a.percent)
}

export const demoDb = {
  // квизы
  listQuizzes: () => allQuizzes().map(stripQuestions),
  getQuiz: (id) => {
    const q = findQuiz(id)
    return q ? stripQuestions(q) : null
  },
  getQuizFull: (id) => findQuiz(id),
  getQuizQuestions: (id) => findQuiz(id)?.questions || [],
  saveBulk,
  deleteQuiz,
  myQuizzes,
  // результаты
  addResult,
  results,
  history,
  statistics,
  leaderboardForQuiz,
}
