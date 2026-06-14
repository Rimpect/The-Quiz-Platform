import React from 'react'

import { useCategories } from '@entities/category'
import { Textarea, Select, CoverUpload, Input } from '@shared'
import { Clock } from 'lucide-react'

import { useQuizStore } from '../../model/quiz.store'

import styles from './QuizStats.module.scss'

const DIFFICULTY_OPTIONS = [
  { value: 'easy', label: 'Лёгкий' },
  { value: 'medium', label: 'Средний' },
  { value: 'hard', label: 'Сложный' },
]

const QUIZ_MODE_OPTIONS = [
  { value: 'single', label: 'Одиночный' },
  { value: 'competitive', label: 'Соревновательный' },
  { value: 'team', label: 'Командный' },
]

export function QuizStats() {
  const quiz = useQuizStore((state) => state.quiz)
  const setField = useQuizStore((state) => state.setField)
  const { categories, loading: categoriesLoading } = useCategories()

  const totalSeconds = quiz.questions.reduce(
    (sum, q) => sum + (q.timeLimitSeconds || 0),
    0,
  )
  const totalMinutes = Math.ceil(totalSeconds / 60)
  const durationLabel =
    totalSeconds > 0
      ? totalMinutes === 1
        ? '~1 мин'
        : `~${totalMinutes} мин`
      : 'без лимита'

  return (
    <div className={styles.container}>
      <div>
        <CoverUpload
          value={quiz.coverUrl}
          onUpload={(url) => setField('coverUrl', url)}
        />

        <div className={styles.fieldGroup}>
          <label htmlFor="quiz-title">Название квиза *</label>

          <Input
            id="quiz-title"
            type="text"
            placeholder="Введите название квиза"
            value={quiz.title}
            maxLength={50}
            onChange={(e) => setField('title', e.target.value)}
          />
        </div>

        <div className={styles.fieldGroup}>
          <label htmlFor="quiz-description">Описание</label>

          <Textarea
            id="quiz-description"
            placeholder="Краткое описание квиза"
            value={quiz.description}
            maxLength={500}
            onChange={(e) => setField('description', e.target.value)}
            className={styles.editorTextarea}
          />
        </div>
      </div>

      <div className={styles.stats}>
        <div className={styles.label}>
          <span>Категория *</span>

          <Select
            value={quiz.categoryId}
            onChange={(e) => setField('categoryId', e.target.value)}
            disabled={categoriesLoading}
          >
            <option value="">Выберите категорию</option>

            {categories.map((cat) => (
              <option key={cat.id} value={String(cat.id)}>
                {cat.category_type}
              </option>
            ))}

            <option value="other">Другое</option>
          </Select>
        </div>

        <div className={styles.label}>
          <span>Сложность *</span>

          <Select
            value={quiz.difficulty}
            onChange={(e) => setField('difficulty', e.target.value)}
          >
            <option value="">Выберите сложность</option>

            {DIFFICULTY_OPTIONS.map((opt) => (
              <option key={opt.value} value={opt.value}>
                {opt.label}
              </option>
            ))}
          </Select>
        </div>

        <div className={styles.label}>
          <span>Тип квиза</span>

          <Select
            value={quiz.quizMode}
            onChange={(e) => setField('quizMode', e.target.value)}
          >
            {QUIZ_MODE_OPTIONS.map((opt) => (
              <option key={opt.value} value={opt.value}>
                {opt.label}
              </option>
            ))}
          </Select>
        </div>

        {quiz.quizMode === 'team' && (
          <div className={styles.label}>
            <label htmlFor="max-team-members">Макс. игроков в команде</label>

            <Input
              id="max-team-members"
              type="number"
              min="1"
              max="50"
              value={quiz.maxTeamMembers || 10}
              onChange={(e) =>
                setField('maxTeamMembers', parseInt(e.target.value) || 10)
              }
            />
          </div>
        )}

        <div className={styles.label}>
          <span>Длительность</span>
          <div className={styles.durationDisplay}>
            <Clock size={16} />
            <span>{durationLabel}</span>
          </div>
        </div>
      </div>
    </div>
  )
}
