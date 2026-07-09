// Мини «REST-сервер» в браузере для демо-режима.
// Перехватывает вызовы client()/request() и отдаёт данные из фикстур.
// Значения возвращаются уже «развёрнутыми» (как их отдают реальные
// client/request после снятия обёртки { data }).
//
// Прогресс прохождения и результаты демо-сессии хранятся в localStorage.

import {
  DEMO_QUIZZES,
  DEMO_CATEGORIES,
  DEMO_LEADERBOARD,
} from './fixtures/quizzes'
import { DEMO_USER, DEMO_STATISTICS, DEMO_ACHIEVEMENTS } from './fixtures/user'

const RESULTS_KEY = 'demo-quiz-results'

// --- искусственная задержка, чтобы были видны состояния загрузки ---
const delay = (ms = 200 + Math.random() * 200) =>
  new Promise((resolve) => setTimeout(resolve, ms))

// --- localStorage helpers ---
const readResults = () => {
  try {
    return JSON.parse(localStorage.getItem(RESULTS_KEY)) || []
  } catch {
    return []
  }
}

const writeResults = (results) => {
  try {
    localStorage.setItem(RESULTS_KEY, JSON.stringify(results))
  } catch {
    /* ignore */
  }
}

const saveResult = (body) => {
  const payload =
    typeof body === 'string' ? JSON.parse(body || '{}') : body || {}
  const quiz = DEMO_QUIZZES.find((q) => q.id === Number(payload.quiz_id))
  const maxScore = payload.max_score || 0
  const record = {
    id: Date.now(),
    quiz_id: Number(payload.quiz_id),
    quiz_title: quiz?.title || 'Квиз',
    score: payload.score || 0,
    max_score: maxScore,
    percent: maxScore ? Math.round(((payload.score || 0) / maxScore) * 100) : 0,
    duration_seconds: payload.duration_seconds || 0,
    created_at: new Date().toISOString(),
  }
  const results = readResults()
  results.unshift(record)
  writeResults(results)
  return record
}

// --- сборка производных данных из фикстур ---
const stripQuestions = (quiz) => {
  const copy = { ...quiz }
  delete copy.questions
  return copy
}
const quizList = () => DEMO_QUIZZES.map(stripQuestions)
const quizById = (id) => {
  const quiz = DEMO_QUIZZES.find((q) => q.id === Number(id))
  return quiz ? stripQuestions(quiz) : null
}
const quizFull = (id) => DEMO_QUIZZES.find((q) => q.id === Number(id)) || null
const quizQuestions = (id) => {
  const quiz = DEMO_QUIZZES.find((q) => q.id === Number(id))
  return quiz ? quiz.questions : []
}

// --- таблица маршрутов: [метод, regExp, handler(matches, options)] ---
const routes = [
  // Квизы
  ['GET', /^\/quizzes$/, () => quizList()],
  ['GET', /^\/quizzes\/categories$/, () => DEMO_CATEGORIES],
  ['GET', /^\/categories$/, () => DEMO_CATEGORIES],
  ['GET', /^\/quizzes\/(\d+)\/full$/, (m) => quizFull(m[1])],
  ['GET', /^\/quizzes\/(\d+)\/questions$/, (m) => quizQuestions(m[1])],
  ['GET', /^\/quizzes\/(\d+)\/leaderboard$/, () => DEMO_LEADERBOARD],
  ['GET', /^\/quizzes\/(\d+)\/edit$/, (m) => quizFull(m[1])],
  ['GET', /^\/quizzes\/(\d+)$/, (m) => quizById(m[1])],
  // Создание/сохранение квиза в демо — просто эхо
  ['POST', /^\/quizzes\/bulk$/, (m, o) => parseBody(o)],
  ['POST', /^\/quizzes\/(\d+)\/bulk$/, (m, o) => parseBody(o)],
  ['POST', /^\/quizzes$/, (m, o) => ({ id: Date.now(), ...parseBody(o) })],
  [
    'PUT',
    /^\/quizzes\/(\d+)$/,
    (m, o) => ({ id: Number(m[1]), ...parseBody(o) }),
  ],
  ['DELETE', /^\/quizzes\/(\d+)$/, () => ({ success: true })],

  // Пользователь
  ['GET', /^\/users\/me\/statistics$/, () => DEMO_STATISTICS],
  ['GET', /^\/users\/me\/quizzes$/, () => quizList().slice(0, 2)],
  ['DELETE', /^\/users\/me\/quizzes\/(\d+)$/, () => ({ success: true })],
  ['GET', /^\/users\/me$/, () => DEMO_USER],
  ['PUT', /^\/users\/me$/, (m, o) => ({ ...DEMO_USER, ...parseBody(o) })],
  ['POST', /^\/users\/me\/change-password$/, () => ({ success: true })],
  ['DELETE', /^\/users\/me$/, () => ({ success: true })],
  ['GET', /^\/users$/, () => [DEMO_USER]],
  ['GET', /^\/users\/(\d+)$/, () => DEMO_USER],

  // Результаты
  ['GET', /^\/quiz-results\/me\/history$/, () => readResults()],
  ['GET', /^\/quiz-results\/me$/, () => readResults()],
  [
    'POST',
    /^\/quiz-results\/save$/,
    (m, o) => {
      saveResult(o.body)
      return { newly_unlocked: [] }
    },
  ],
  ['POST', /^\/quiz-results$/, (m, o) => saveResult(o.body)],
  ['GET', /^\/quiz-results\/quiz\/(\d+)\/leaderboard$/, () => DEMO_LEADERBOARD],
  [
    'POST',
    /^\/quiz-results\/(\d+)\/complete$/,
    (m) => ({ id: Number(m[1]), completed: true }),
  ],
  ['GET', /^\/quiz-results\/(\d+)$/, (m) => ({ id: Number(m[1]) })],

  // Достижения
  ['GET', /^\/achievements$/, () => DEMO_ACHIEVEMENTS],
  ['POST', /^\/achievements\/check$/, () => ({ newly_unlocked: [] })],
  ['POST', /^\/achievements\/(\d+)\/unlock$/, () => ({ success: true })],

  // Админка (демо-пользователь — admin)
  ['GET', /^\/admin\/pending$/, () => []],
  ['GET', /^\/admin\/quizzes$/, () => quizList()],
  ['GET', /^\/admin\/rejected$/, () => []],
  ['POST', /^\/admin\/quizzes\/(\d+)\/approve$/, () => ({ success: true })],
  ['POST', /^\/admin\/quizzes\/(\d+)\/reject$/, () => ({ success: true })],
  ['DELETE', /^\/admin\/quizzes\/(\d+)$/, () => ({ success: true })],

  // Медиа — в демо загрузка недоступна, возвращаем заглушку
  ['POST', /^\/media\//, () => ({ url: null, path: null })],
  ['GET', /^\/media\//, () => null],

  // Авторизация — в демо не используется, но на всякий случай
  [
    'POST',
    /^\/auth\/login$/,
    () => ({
      access_token: 'demo-token',
      user_id: DEMO_USER.id,
      nickname: DEMO_USER.nickname,
      role: DEMO_USER.role,
      photo_profile: null,
    }),
  ],
  ['POST', /^\/auth\/refresh$/, () => ({ access_token: 'demo-token' })],
  ['POST', /^\/auth\/logout$/, () => ({ success: true })],
  ['GET', /^\/auth\/sessions$/, () => []],
  ['GET', /^\/auth\/history$/, () => []],
]

const parseBody = (options) => {
  try {
    return typeof options?.body === 'string'
      ? JSON.parse(options.body || '{}')
      : options?.body || {}
  } catch {
    return {}
  }
}

export const mockRouter = async (endpoint, options = {}) => {
  const method = (options.method || 'GET').toUpperCase()
  const path = endpoint.split('?')[0]

  await delay()

  for (const [routeMethod, pattern, handler] of routes) {
    if (routeMethod !== method) continue
    const match = path.match(pattern)
    if (match) {
      return handler(match, options)
    }
  }

  // Мультиплеер и прочее серверное в демо не поддерживается
  if (path.startsWith('/game/')) {
    throw new Error('Мультиплеер недоступен в демо-версии')
  }

  console.warn(`[demo] Не найден mock для ${method} ${path}`)
  return null
}
