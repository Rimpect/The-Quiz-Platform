import React from 'react'

import { Input, Textarea, Select, CoverUpload } from '@shared'

import styles from './QuizStats.module.scss'

export function QuizStats() {
  return (
    <div className={styles.container}>
      <div>
        <CoverUpload></CoverUpload>
        <div className={styles.fieldGroup}>
          <label htmlFor="quiz-title">Название квиза *</label>
          <Input
            id="quiz-title"
            type="text"
            placeholder="Введите название квиза"
          />
        </div>

        <div className={styles.fieldGroup}>
          <label htmlFor="quiz-description">Описание</label>
          <Textarea
            id="quiz-description"
            type="text"
            placeholder="Краткое описание квиза"
          />
        </div>
      </div>

      <div className={styles.stats}>
        <div className={styles.label}>
          <span>Категория *</span>
          <Select>
            <option value="">Выберите опцию</option>
            <option value="1">Опция 1</option>
            <option value="2">Опция 2</option>
            <option value="3">Опция 3</option>
          </Select>
        </div>

        <div className={styles.label}>
          <span>Сложность *</span>
          <Select>
            <option value="">Выберите опцию</option>
            <option value="1">Опция 1</option>
            <option value="2">Опция 2</option>
            <option value="3">Опция 3</option>
          </Select>
        </div>

        <div className={styles.label}>
          <span>Длительность (мин)</span>
          <Input
            type="number"
            placeholder="10"
            defaultValue={10}
            min={1}
            step={1}
          />
        </div>
      </div>
    </div>
  )
}
