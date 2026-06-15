import { useMemo, useState } from 'react'

export const QUESTION_MIN = 1
export const QUESTION_MAX = 100
export const DURATION_MIN = 0
export const DURATION_MAX = 180

const createInitialFilters = () => ({
  categories: [],
  difficulty: null,
  typeQuestions: [],
  mediaType: [],
  numberOfQuestionsFrom: QUESTION_MIN,
  numberOfQuestionsTo: QUESTION_MAX,
  durationFrom: DURATION_MIN,
  durationTo: DURATION_MAX,
  typeQuiz: null,
})

const clamp = (value, min, max) => {
  const n = Number(value)
  return Math.min(max, Math.max(min, Number.isNaN(n) ? min : n))
}

export function useFilterDraft(filter, { onApply, onReset, onClose }) {
  const [draftFilters, setDraftFilters] = useState(filter ?? createInitialFilters())

  const toggleArrayValue = (key, value) => {
    setDraftFilters((current) => {
      const values = current[key] || []
      return {
        ...current,
        [key]: values.includes(value)
          ? values.filter((item) => item !== value)
          : [...values, value],
      }
    })
  }

  const setDifficulty = (value) => {
    setDraftFilters((current) => ({
      ...current,
      difficulty: value === 'all' ? null : value,
    }))
  }

  const setQuestionCount = (key, value) => {
    setDraftFilters((current) => ({
      ...current,
      [key]: clamp(value, QUESTION_MIN, QUESTION_MAX),
    }))
  }

  const setDuration = (key, value) => {
    setDraftFilters((current) => ({
      ...current,
      [key]: clamp(value, DURATION_MIN, DURATION_MAX),
    }))
  }

  const validationError = useMemo(() => {
    if (draftFilters.numberOfQuestionsFrom > draftFilters.numberOfQuestionsTo) {
      return 'Количество вопросов: «От» не может быть больше «До».'
    }
    if (draftFilters.durationFrom > draftFilters.durationTo) {
      return 'Длительность: «От» не может быть больше «До».'
    }
    return null
  }, [draftFilters])

  const reset = () => {
    setDraftFilters(createInitialFilters())
    if (onReset) onReset()
  }

  const apply = () => {
    if (validationError) return
    if (onApply) onApply(draftFilters)
    onClose()
  }

  return {
    draftFilters,
    toggleArrayValue,
    setDifficulty,
    setQuestionCount,
    setDuration,
    validationError,
    reset,
    apply,
  }
}
