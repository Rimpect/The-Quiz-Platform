import React from 'react'

import { Button } from '@shared'
import { X, Image, Video, Music } from 'lucide-react'

import styles from './ModalFilter.module.scss'

export function ModalFilter({ isOpen, onClose }) {
  if (!isOpen) return null

  const categories = [
    'История',
    'Наука',
    'География',
    'Кино',
    'Музыка',
    'Спорт',
    'Технологии',
    'Еда',
    'Природа',
    'Общие',
    'Логика',
    'Культура',
  ]

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
              {categories.map((category) => (
                <div key={category} className={styles.checkboxItem}>
                  <input
                    type="checkbox"
                    id={category}
                    className={styles.checkboxInput}
                  />
                  <label htmlFor={category} className={styles.checkboxLabel}>
                    {category}
                  </label>
                </div>
              ))}
            </div>
          </div>

          <div className={styles.section}>
            <label className={styles.label}>Сложность</label>
            <div className={styles.radioGroup}>
              <div className={styles.radioItem}>
                <input
                  type="radio"
                  name="difficulty"
                  id="all"
                  value="all"
                  className={styles.radioInput}
                />
                <label htmlFor="all" className={styles.radioLabel}>
                  Все
                </label>
              </div>
              <div className={styles.radioItem}>
                <input
                  type="radio"
                  name="difficulty"
                  id="easy"
                  value="Легкий"
                  className={styles.radioInput}
                />
                <label htmlFor="easy" className={styles.radioLabel}>
                  Легкий
                </label>
              </div>
              <div className={styles.radioItem}>
                <input
                  type="radio"
                  name="difficulty"
                  id="medium"
                  value="Средний"
                  className={styles.radioInput}
                />
                <label htmlFor="medium" className={styles.radioLabel}>
                  Средний
                </label>
              </div>
              <div className={styles.radioItem}>
                <input
                  type="radio"
                  name="difficulty"
                  id="hard"
                  value="Сложный"
                  className={styles.radioInput}
                />
                <label htmlFor="hard" className={styles.radioLabel}>
                  Сложный
                </label>
              </div>
            </div>
          </div>

          <div className={styles.section}>
            <label className={styles.label}>Тип вопросов</label>
            <div className={styles.checkboxGroup}>
              <div className={styles.checkboxItem}>
                <input
                  type="checkbox"
                  id="single"
                  className={styles.checkboxInput}
                />
                <label htmlFor="single" className={styles.checkboxLabel}>
                  Одиночный выбор
                </label>
              </div>
              <div className={styles.checkboxItem}>
                <input
                  type="checkbox"
                  id="multiple"
                  className={styles.checkboxInput}
                />
                <label htmlFor="multiple" className={styles.checkboxLabel}>
                  Множественный выбор
                </label>
              </div>
            </div>
          </div>

          <div className={styles.section}>
            <label className={styles.label}>Содержит медиа</label>
            <div className={styles.checkboxGroup}>
              <div className={styles.checkboxItem}>
                <input
                  type="checkbox"
                  id="image"
                  className={styles.checkboxInput}
                />
                <Image className={styles.mediaIcon} />
                <label htmlFor="image" className={styles.checkboxLabel}>
                  Изображения
                </label>
              </div>
              <div className={styles.checkboxItem}>
                <input
                  type="checkbox"
                  id="video"
                  className={styles.checkboxInput}
                />
                <Video className={styles.mediaIcon} />
                <label htmlFor="video" className={styles.checkboxLabel}>
                  Видео
                </label>
              </div>
              <div className={styles.checkboxItem}>
                <input
                  type="checkbox"
                  id="audio"
                  className={styles.checkboxInput}
                />
                <Music className={styles.mediaIcon} />
                <label htmlFor="audio" className={styles.checkboxLabel}>
                  Аудио
                </label>
              </div>
            </div>
          </div>

          <div className={styles.section}>
            <label className={styles.label}>Количество вопросов: 1 - 20</label>
            <div className={styles.sliderContainer}>
              <input
                type="range"
                min="1"
                max="50"
                step="1"
                defaultValue="20"
                className={styles.sliderInput}
              />
              <div className={styles.sliderLabels}>
                <span>1</span>
                <span>50</span>
              </div>
            </div>
          </div>

          <div className={styles.section}>
            <label className={styles.label}>Длительность (мин): 5 - 60</label>
            <div className={styles.sliderContainer}>
              <input
                type="range"
                min="5"
                max="120"
                step="5"
                defaultValue="60"
                className={styles.sliderInput}
              />
              <div className={styles.sliderLabels}>
                <span>5</span>
                <span>120</span>
              </div>
            </div>
          </div>
        </div>

        <div className={styles.footer}>
          <Button variant="white" fullWidth>
            {' '}
            Сбросить все
          </Button>
          <Button variant="black" fullWidth>
            {' '}
            Применить фильтры
          </Button>
        </div>
      </div>
    </div>
  )
}
