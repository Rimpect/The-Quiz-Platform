import { useEffect } from 'react'
import {
  Info,
  CheckCircle,
  Image,
  Video,
  Music,
  ListChecks,
  X,
} from 'lucide-react'
import styles from './ModalHelp.module.scss'

export function ModalHelp({ onClose }) {
  // Блокировка скролла фона и обработка ESC
  useEffect(() => {
    document.body.style.overflow = 'hidden'

    const handleEsc = (e) => {
      if (e.key === 'Escape') {
        onClose()
      }
    }

    window.addEventListener('keydown', handleEsc)

    return () => {
      document.body.style.overflow = 'unset'
      window.removeEventListener('keydown', handleEsc)
    }
  }, [onClose])

  const handleContentClick = (e) => {
    e.stopPropagation()
  }

  return (
    <div className={styles.helpOverlay} onClick={onClose}>
      <div className={styles.helpModal} onClick={handleContentClick}>
        <button className={styles.closeBtn} onClick={onClose}>
          <X size={24} />
        </button>

        <div className={styles.helpHeader}>
          <Info className={styles.headerIcon} />
          <h2 className={styles.helpTitle}>Руководство по созданию квизов</h2>
        </div>

        <div className={styles.helpContent}>
          {/* Типы вопросов */}
          <section className={styles.helpSection}>
            <h3 className={styles.sectionTitle}>Типы вопросов</h3>
            <div className={styles.cardsContainer}>
              <div className={`${styles.helpCard} ${styles.cardBlue}`}>
                <CheckCircle color="blue" className={styles.cardIcon} />
                <div>
                  <p className={styles.cardTitle}>Один правильный ответ</p>
                  <p className={styles.cardDesc}>
                    Пользователь может выбрать только один вариант. Используйте
                    радио-кнопки.
                  </p>
                </div>
              </div>

              <div className={`${styles.helpCard} ${styles.cardGreen}`}>
                <ListChecks color="green" className={styles.cardIcon} />
                <div>
                  <p className={styles.cardTitle}>
                    Несколько правильных ответов
                  </p>
                  <p className={styles.cardDesc}>
                    Пользователь может выбрать несколько вариантов. Используйте
                    чекбоксы.
                  </p>
                  <p className={styles.cardHint}>
                    💡 Частичное начисление баллов: если выбраны не все
                    правильные ответы, баллы начисляются пропорционально
                    (например, 2 из 3 правильных = 67% баллов)
                  </p>
                </div>
              </div>
            </div>
          </section>

          {/* Медиа файлы */}
          <section className={styles.helpSection}>
            <h3 className={styles.sectionTitle}>Медиа файлы</h3>
            <div className={styles.cardsContainer}>
              <div className={`${styles.helpCard} ${styles.cardPurple}`}>
                <Image color="purple" className={styles.cardIcon} />
                <div>
                  <p className={styles.cardTitle}>Изображения</p>
                  <p className={styles.cardDesc}>
                    Добавляйте картинки для визуальных вопросов (JPG, PNG, GIF)
                  </p>
                </div>
              </div>

              <div className={`${styles.helpCard} ${styles.cardPink}`}>
                <Video color="violet" className={styles.cardIcon} />
                <div>
                  <p className={styles.cardTitle}>Видео</p>
                  <p className={styles.cardDesc}>
                    Загружайте видео для вопросов о фильмах, событиях и т.д.
                    (MP4, WebM)
                  </p>
                </div>
              </div>

              <div className={`${styles.helpCard} ${styles.cardOrange}`}>
                <Music color="orange" className={styles.cardIcon} />
                <div>
                  <p className={styles.cardTitle}>Аудио</p>
                  <p className={styles.cardDesc}>
                    Добавляйте аудио файлы для музыкальных квизов (MP3, WAV,
                    OGG)
                  </p>
                </div>
              </div>
            </div>
          </section>

          {/* Система баллов */}
          <section className={styles.helpSection}>
            <h3 className={styles.sectionTitle}>Система баллов</h3>
            <div className={styles.scoreWrapper}>
              <div className={styles.scoreItem}>
                <strong>Одиночный выбор:</strong> Полные баллы за правильный
                ответ, 0 за неправильный
              </div>
              <div className={styles.scoreItem}>
                <strong>Множественный выбор:</strong> Баллы начисляются
                пропорционально
              </div>
              <ul className={styles.scoreList}>
                <li>✓ Все правильные выбраны = 100% баллов</li>
                <li>
                  ✓ 2 из 3 правильных выбраны = 67% баллов (округление вниз)
                </li>
                <li>✓ Выбран хотя бы 1 неправильный = 0 баллов</li>
                <li>✓ Ничего не выбрано = 0 баллов</li>
              </ul>
            </div>
          </section>

          {/* Примеры */}
          <section className={styles.helpSection}>
            <h3 className={styles.sectionTitle}>Примеры использования</h3>
            <div className={styles.examplesList}>
              <p>
                📸 <strong>Квиз с изображениями:</strong> "Угадай
                достопримечательность по фото"
              </p>
              <p>
                🎬 <strong>Квиз с видео:</strong> "Угадай фильм по отрывку"
              </p>
              <p>
                🎵 <strong>Квиз с аудио:</strong> "Угадай песню или композитора"
              </p>
              <p>
                ✅ <strong>Множественный выбор:</strong> "Выберите все столицы
                европейских стран"
              </p>
            </div>
          </section>

          {/* Совет */}
          <div className={styles.tipBox}>
            <p>
              <strong>Совет:</strong> Для лучшего опыта используйте файлы
              небольшого размера (изображения до 2МБ, видео до 10МБ, аудио до
              5МБ)
            </p>
          </div>
        </div>

        <div className={styles.helpFooter}>
          <button className={styles.doneBtn} onClick={onClose}>
            Понятно
          </button>
        </div>
      </div>
    </div>
  )
}
