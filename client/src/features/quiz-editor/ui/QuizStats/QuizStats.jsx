import React from 'react'

import { Input, Textarea, Select, CoverUpload } from '@shared'

import { useQuizStore } from '../../model/quiz.store'

import styles from './QuizStats.module.scss'

export function QuizStats() {
  const quiz = useQuizStore((state) => state.quiz)

  const setField = useQuizStore((state) => state.setField)

  return (
    <div className={styles.container}>
      <div>
        <CoverUpload />

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
            maxLength={100}
            onChange={(e) => setField('description', e.target.value)}
            className={styles.editorTextarea}
          />
        </div>
      </div>

      <div className={styles.stats}>
        <div className={styles.label}>
          <span>Категория *</span>

          <Select
            value={quiz.category}
            onChange={(e) => setField('category', e.target.value)}
          >
            <option value="">Выберите опцию</option>

            <option value="frontend">Frontend</option>

            <option value="backend">Backend</option>
          </Select>
        </div>

        <div className={styles.label}>
          <span>Сложность *</span>

          <Select
            value={quiz.difficulty}
            onChange={(e) => setField('difficulty', e.target.value)}
          >
            <option value="">Выберите сложность</option>

            <option value="easy">Easy</option>

            <option value="medium">Medium</option>
          </Select>
        </div>

        <div className={styles.label}>
          <span>Длительность (мин)</span>

          <Input
            type="number"
            value={quiz.duration}
            onChange={(e) => setField('duration', Number(e.target.value))}
            min={1}
            step={1}
          />
        </div>
      </div>
    </div>
  )
}
