// Демо-пользователь. В демо-режиме он «залогинен» сразу и имеет роль admin,
// чтобы была доступна админ-панель.

export const DEMO_USER = {
  id: 1,
  nickname: 'Демо-пользователь',
  name: 'Демо-пользователь',
  email: 'demo@example.com',
  role: 'admin',
  photo_profile: null,
  created_at: '2024-01-01T00:00:00Z',
}

// Ответ для /users/me/statistics
export const DEMO_STATISTICS = {
  total_quizzes_completed: 12,
  average_score: 78,
  best_result: 95,
  total_minutes: 64,
}

// Достижения: карта id -> unlocked (см. useAchievements)
export const DEMO_ACHIEVEMENTS = {
  achievements: {
    1: true,
    2: true,
    3: false,
  },
}
