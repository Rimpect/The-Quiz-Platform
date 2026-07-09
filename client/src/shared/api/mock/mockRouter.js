// Мини «REST-сервер» в браузере для демо-режима.
// Перехватывает вызовы client()/request() и отдаёт данные из фикстур/localStorage.
// Значения возвращаются уже «развёрнутыми» (как их отдают реальные
// client/request после снятия обёртки { data }).
//
// Данные (результаты прохождения, созданные квизы) хранит demoDb в localStorage,
// поэтому история/статистика/лучший результат согласованы, как в продакшене.

import { demoDb } from './demoDb'
import { DEMO_CATEGORIES } from './fixtures/quizzes'
import { DEMO_USER, DEMO_ACHIEVEMENTS } from './fixtures/user'

// --- искусственная задержка, чтобы были видны состояния загрузки ---
const delay = (ms = 200 + Math.random() * 200) =>
  new Promise((resolve) => setTimeout(resolve, ms))

const parseBody = (options) => {
  try {
    return typeof options?.body === 'string'
      ? JSON.parse(options.body || '{}')
      : options?.body || {}
  } catch {
    return {}
  }
}

// --- таблица маршрутов: [метод, regExp, handler(matches, options)] ---
const routes = [
  // Квизы
  ['GET', /^\/quizzes$/, () => demoDb.listQuizzes()],
  ['GET', /^\/quizzes\/categories$/, () => DEMO_CATEGORIES],
  ['GET', /^\/categories$/, () => DEMO_CATEGORIES],
  ['GET', /^\/quizzes\/(\d+)\/full$/, (m) => demoDb.getQuizFull(m[1])],
  [
    'GET',
    /^\/quizzes\/(\d+)\/questions$/,
    (m) => demoDb.getQuizQuestions(m[1]),
  ],
  [
    'GET',
    /^\/quizzes\/(\d+)\/leaderboard$/,
    (m) => demoDb.leaderboardForQuiz(m[1]),
  ],
  ['GET', /^\/quizzes\/(\d+)\/edit$/, (m) => demoDb.getQuizFull(m[1])],
  ['GET', /^\/quizzes\/(\d+)$/, (m) => demoDb.getQuiz(m[1])],
  // Создание / редактирование квиза — сохраняется в localStorage
  ['POST', /^\/quizzes\/bulk$/, (m, o) => demoDb.saveBulk(o.body)],
  ['POST', /^\/quizzes\/(\d+)\/bulk$/, (m, o) => demoDb.saveBulk(o.body, m[1])],
  ['PUT', /^\/quizzes\/(\d+)\/bulk$/, (m, o) => demoDb.saveBulk(o.body, m[1])],
  ['POST', /^\/quizzes$/, (m, o) => ({ id: Date.now(), ...parseBody(o) })],
  [
    'PUT',
    /^\/quizzes\/(\d+)$/,
    (m, o) => ({ id: Number(m[1]), ...parseBody(o) }),
  ],
  ['DELETE', /^\/quizzes\/(\d+)$/, () => ({ success: true })],

  // Пользователь
  ['GET', /^\/users\/me\/statistics$/, () => demoDb.statistics()],
  ['GET', /^\/users\/me\/quizzes$/, () => demoDb.myQuizzes()],
  ['DELETE', /^\/users\/me\/quizzes\/(\d+)$/, (m) => demoDb.deleteQuiz(m[1])],
  ['GET', /^\/users\/me$/, () => DEMO_USER],
  ['PUT', /^\/users\/me$/, (m, o) => ({ ...DEMO_USER, ...parseBody(o) })],
  ['POST', /^\/users\/me\/change-password$/, () => ({ success: true })],
  ['DELETE', /^\/users\/me$/, () => ({ success: true })],
  ['GET', /^\/users$/, () => [DEMO_USER]],
  ['GET', /^\/users\/(\d+)$/, () => DEMO_USER],

  // Результаты
  ['GET', /^\/quiz-results\/me\/history$/, () => demoDb.history()],
  ['GET', /^\/quiz-results\/me$/, () => demoDb.results()],
  [
    'POST',
    /^\/quiz-results\/save$/,
    (m, o) => {
      demoDb.addResult(o.body)
      return { newly_unlocked: [] }
    },
  ],
  ['POST', /^\/quiz-results$/, (m, o) => demoDb.addResult(o.body)],
  [
    'GET',
    /^\/quiz-results\/quiz\/(\d+)\/leaderboard$/,
    (m) => demoDb.leaderboardForQuiz(m[1]),
  ],
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
  ['GET', /^\/admin\/quizzes$/, () => demoDb.listQuizzes()],
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
