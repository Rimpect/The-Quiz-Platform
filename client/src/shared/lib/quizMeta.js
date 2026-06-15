// Единые подписи и варианты бейджей для квизов (карточка, описание, и т.п.)

export const QUIZ_MODE_LABELS = {
  single: 'Соло',
  solo: 'Соло',
  team: 'Командный',
  competitive: 'Рейтинговый',
}

const DIFFICULTY = {
  easy: { variant: 'easy', label: 'Лёгкий' },
  medium: { variant: 'medium', label: 'Средний' },
  hard: { variant: 'hard', label: 'Сложный' },
}

// Принимает и английские ключи (easy/medium/hard), и русские подписи
const ALIASES = {
  лёгкий: 'easy',
  легкий: 'easy',
  средний: 'medium',
  сложный: 'hard',
}

export const getDifficulty = (value) => {
  const raw = String(value || '').toLowerCase()
  const key = ALIASES[raw] || raw
  return DIFFICULTY[key] || DIFFICULTY.easy
}
