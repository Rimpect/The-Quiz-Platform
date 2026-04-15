import React from 'react'

import { X, Image, Video, Music } from 'lucide-react'
import './ModalFilter.scss'

const ModalFilter = ({ isOpen, onClose }) => {
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
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2 className="modal-title">Фильтры квизов</h2>
          <button className="modal-close" onClick={onClose}>
            <X className="modal-close-icon" />
          </button>
        </div>

        <div className="modal-body">
          <div className="filter-section">
            <label className="filter-label">Категории</label>
            <div className="categories-grid">
              {categories.map((category) => (
                <div key={category} className="checkbox-item">
                  <input
                    type="checkbox"
                    id={category}
                    className="checkbox-input"
                  />
                  <label htmlFor={category} className="checkbox-label">
                    {category}
                  </label>
                </div>
              ))}
            </div>
          </div>

          <div className="filter-section">
            <label className="filter-label">Сложность</label>
            <div className="radio-group">
              <div className="radio-item">
                <input
                  type="radio"
                  name="difficulty"
                  id="all"
                  value="all"
                  className="radio-input"
                />
                <label htmlFor="all" className="radio-label">
                  Все
                </label>
              </div>
              <div className="radio-item">
                <input
                  type="radio"
                  name="difficulty"
                  id="easy"
                  value="Легкий"
                  className="radio-input"
                />
                <label htmlFor="easy" className="radio-label">
                  Легкий
                </label>
              </div>
              <div className="radio-item">
                <input
                  type="radio"
                  name="difficulty"
                  id="medium"
                  value="Средний"
                  className="radio-input"
                />
                <label htmlFor="medium" className="radio-label">
                  Средний
                </label>
              </div>
              <div className="radio-item">
                <input
                  type="radio"
                  name="difficulty"
                  id="hard"
                  value="Сложный"
                  className="radio-input"
                />
                <label htmlFor="hard" className="radio-label">
                  Сложный
                </label>
              </div>
            </div>
          </div>

          <div className="filter-section">
            <label className="filter-label">Тип вопросов</label>
            <div className="checkbox-group">
              <div className="checkbox-item">
                <input type="checkbox" id="single" className="checkbox-input" />
                <label htmlFor="single" className="checkbox-label">
                  Одиночный выбор
                </label>
              </div>
              <div className="checkbox-item">
                <input
                  type="checkbox"
                  id="multiple"
                  className="checkbox-input"
                />
                <label htmlFor="multiple" className="checkbox-label">
                  Множественный выбор
                </label>
              </div>
            </div>
          </div>

          <div className="filter-section">
            <label className="filter-label">Содержит медиа</label>
            <div className="checkbox-group">
              <div className="checkbox-item">
                <input type="checkbox" id="image" className="checkbox-input" />
                <Image className="media-icon" />
                <label htmlFor="image" className="checkbox-label">
                  Изображения
                </label>
              </div>
              <div className="checkbox-item">
                <input type="checkbox" id="video" className="checkbox-input" />
                <Video className="media-icon" />
                <label htmlFor="video" className="checkbox-label">
                  Видео
                </label>
              </div>
              <div className="checkbox-item">
                <input type="checkbox" id="audio" className="checkbox-input" />
                <Music className="media-icon" />
                <label htmlFor="audio" className="checkbox-label">
                  Аудио
                </label>
              </div>
            </div>
          </div>

          {/* Количество вопросов */}
          <div className="filter-section">
            <label className="filter-label">Количество вопросов: 1 - 20</label>
            <div className="slider-container">
              <input
                type="range"
                min="1"
                max="50"
                step="1"
                defaultValue="20"
                className="slider-input"
              />
              <div className="slider-labels">
                <span>1</span>
                <span>50</span>
              </div>
            </div>
          </div>

          <div className="filter-section">
            <label className="filter-label">Длительность (мин): 5 - 60</label>
            <div className="slider-container">
              <input
                type="range"
                min="5"
                max="120"
                step="5"
                defaultValue="60"
                className="slider-input"
              />
              <div className="slider-labels">
                <span>5</span>
                <span>120</span>
              </div>
            </div>
          </div>
        </div>

        <div className="modal-footer">
          <button className="modal-button modal-button--outline">
            Сбросить все
          </button>
          <button className="modal-button modal-button--primary">
            Применить фильтры
          </button>
        </div>
      </div>
    </div>
  )
}

export default ModalFilter
