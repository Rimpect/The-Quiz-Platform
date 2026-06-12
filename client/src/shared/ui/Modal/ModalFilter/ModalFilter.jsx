import React, { useMemo, useState } from 'react'

import { useCategories } from '@entities/category/model/useCategories'
import { Button, Input } from '@shared'
import { X, Image, Video, Music } from 'lucide-react'

import styles from './ModalFilter.module.scss'

const QUESTION_MIN = 1
const QUESTION_MAX = 100
const DURATION_MIN = 0
const DURATION_MAX = 180

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

export function ModalFilter({ isOpen, onClose, onApply, onReset, filter }) {
  if (!isOpen) return null
  return (
    <ModalFilterContent
      onClose={onClose}
      onApply={onApply}
      onReset={onReset}
      filter={filter}
    />
  )
}

function ModalFilterContent({ onClose, onApply, onReset, filter }) {
  const [draftFilters, setDraftFilters] = useState(
    filter ?? createInitialFilters(),
  )
  const { categories: dbCategories } = useCategories()

  const categoryNames = dbCategories
    .map((c) => c.category_type || c)
    .filter(Boolean)

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

  const handleDifficultyChange = (value) => {
    setDraftFilters((current) => ({
      ...current,
      difficulty: value === 'all' ? null : value,
    }))
  }

  const handleNumberOfQuestionsChange = (key, value) => {
    const n = Number(value)
    setDraftFilters((current) => ({
      ...current,
      [key]: Math.min(
        QUESTION_MAX,
        Math.max(QUESTION_MIN, Number.isNaN(n) ? QUESTION_MIN : n),
      ),
    }))
  }

  const handleDurationChange = (key, value) => {
    const n = Number(value)
    setDraftFilters((current) => ({
      ...current,
      [key]: Math.min(
        DURATION_MAX,
        Math.max(DURATION_MIN, Number.isNaN(n) ? DURATION_MIN : n),
      ),
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

  const handleReset = () => {
    setDraftFilters(createInitialFilters())
    if (onReset) onReset()
  }

  const handleApply = () => {
    if (validationError) return
    if (onApply) onApply(draftFilters)
    onClose()
  }

  return (
    <div className={styles.overlay} onClick={onClose}>
      <div className={styles.content} onClick={(e) => e.stopPropagation()}>
        <div className={styles.header}>
          <h2 className={styles.title}>Фильтры квизов</h2>
          <button className={styles.closeBtn} onClick={onClose}>
            <X className={styles.closeIcon} />
          </button>
        </div>

        <div className={styles.body}>
          <div className={styles.section}>
            <label className={styles.label}>Категории</label>
            <div className={styles.categoriesGrid}>
              {categoryNames.map((category) => (
                <div key={category} className={styles.checkboxItem}>
                  <input
                    type="checkbox"
                    id={`cat-${category}`}
                    className={styles.checkboxInput}
                    checked={draftFilters.categories.includes(category)}
                    onChange={() => toggleArrayValue('categories', category)}
                  />
                  <label
                    htmlFor={`cat-${category}`}
                    className={styles.checkboxLabel}
                  >
                    {category}
                  </label>
                </div>
              ))}
            </div>
          </div>

          <div className={styles.section}>
            <label className={styles.label}>Сложность</label>
            <div className={styles.radioGroup}>
              {[
                { id: 'diff-all', label: 'Все', value: 'all' },
                { id: 'diff-easy', label: 'Лёгкий', value: 'easy' },
                { id: 'diff-medium', label: 'Средний', value: 'medium' },
                { id: 'diff-hard', label: 'Сложный', value: 'hard' },
              ].map((option) => (
                <div key={option.id} className={styles.radioItem}>
                  <input
                    type="radio"
                    name="difficulty"
                    id={option.id}
                    value={option.value}
                    className={styles.radioInput}
                    checked={
                      option.value === 'all'
                        ? draftFilters.difficulty === null
                        : draftFilters.difficulty === option.value
                    }
                    onChange={() => handleDifficultyChange(option.value)}
                  />
                  <label htmlFor={option.id} className={styles.radioLabel}>
                    {option.label}
                  </label>
                </div>
              ))}
            </div>
          </div>

          <div className={styles.section}>
            <label className={styles.label}>Тип вопросов</label>
            <div className={styles.checkboxGroup}>
              {[
                { id: 'tq-single', label: 'Одиночный выбор', value: 'single' },
                {
                  id: 'tq-multiple',
                  label: 'Множественный выбор',
                  value: 'multiple',
                },
              ].map((option) => (
                <div key={option.id} className={styles.checkboxItem}>
                  <input
                    type="checkbox"
                    id={option.id}
                    className={styles.checkboxInput}
                    checked={draftFilters.typeQuestions.includes(option.value)}
                    onChange={() =>
                      toggleArrayValue('typeQuestions', option.value)
                    }
                  />
                  <label htmlFor={option.id} className={styles.checkboxLabel}>
                    {option.label}
                  </label>
                </div>
              ))}
            </div>
          </div>

          <div className={styles.section}>
            <label className={styles.label}>Содержит медиа</label>
            <div className={styles.checkboxGroup}>
              {[
                {
                  id: 'media-image',
                  label: 'Изображения',
                  value: 'image',
                  icon: <Image className={styles.mediaIcon} />,
                },
                {
                  id: 'media-video',
                  label: 'Видео',
                  value: 'video',
                  icon: <Video className={styles.mediaIcon} />,
                },
                {
                  id: 'media-audio',
                  label: 'Аудио',
                  value: 'audio',
                  icon: <Music className={styles.mediaIcon} />,
                },
              ].map((option) => (
                <div key={option.id} className={styles.checkboxItem}>
                  <input
                    type="checkbox"
                    id={option.id}
                    className={styles.checkboxInput}
                    checked={draftFilters.mediaType.includes(option.value)}
                    onChange={() => toggleArrayValue('mediaType', option.value)}
                  />
                  {option.icon}
                  <label htmlFor={option.id} className={styles.checkboxLabel}>
                    {option.label}
                  </label>
                </div>
              ))}
            </div>
          </div>

          <div className={styles.section}>
            <label className={styles.label}>Количество вопросов</label>
            <div className={styles.rangeRow}>
              <div className={styles.rangeField}>
                <label className={styles.rangeLabel}>От</label>
                <Input
                  type="number"
                  min={QUESTION_MIN}
                  max={QUESTION_MAX}
                  value={draftFilters.numberOfQuestionsFrom}
                  className={styles.numberInput}
                  onChange={(e) =>
                    handleNumberOfQuestionsChange(
                      'numberOfQuestionsFrom',
                      e.target.value,
                    )
                  }
                />
              </div>
              <div className={styles.rangeField}>
                <label className={styles.rangeLabel}>До</label>
                <Input
                  type="number"
                  min={QUESTION_MIN}
                  max={QUESTION_MAX}
                  value={draftFilters.numberOfQuestionsTo}
                  className={styles.numberInput}
                  onChange={(e) =>
                    handleNumberOfQuestionsChange(
                      'numberOfQuestionsTo',
                      e.target.value,
                    )
                  }
                />
              </div>
            </div>
            <p className={styles.hintText}>
              Диапазон: {QUESTION_MIN}–{QUESTION_MAX} вопросов
            </p>
          </div>

          <div className={styles.section}>
            <label className={styles.label}>Длительность (мин)</label>
            <div className={styles.rangeRow}>
              <div className={styles.rangeField}>
                <label className={styles.rangeLabel}>От</label>
                <Input
                  type="number"
                  min={DURATION_MIN}
                  max={DURATION_MAX}
                  value={draftFilters.durationFrom}
                  className={styles.numberInput}
                  onChange={(e) =>
                    handleDurationChange('durationFrom', e.target.value)
                  }
                />
              </div>
              <div className={styles.rangeField}>
                <label className={styles.rangeLabel}>До</label>
                <Input
                  type="number"
                  min={DURATION_MIN}
                  max={DURATION_MAX}
                  value={draftFilters.durationTo}
                  className={styles.numberInput}
                  onChange={(e) =>
                    handleDurationChange('durationTo', e.target.value)
                  }
                />
              </div>
            </div>
            <p className={styles.hintText}>
              Диапазон: {DURATION_MIN}–{DURATION_MAX} минут
            </p>
          </div>

          {validationError && (
            <p className={styles.errorText}>{validationError}</p>
          )}
        </div>

        <div className={styles.footer}>
          <Button variant="white" fullWidth onClick={handleReset}>
            Сбросить все
          </Button>
          <Button
            variant="black"
            fullWidth
            onClick={handleApply}
            disabled={Boolean(validationError)}
          >
            Применить фильтры
          </Button>
        </div>
      </div>
    </div>
  )
}
