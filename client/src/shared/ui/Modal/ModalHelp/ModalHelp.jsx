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
        <div className={styles.helpHeader}>
          <div className={styles.headerIconBox}>
            <Info size={26} />
          </div>
          <div>
            <h2 className={styles.helpTitle}>Создание квизов</h2>
            <p className={styles.helpSubtitle}>
              Краткое руководство по типам вопросов, медиа и баллам
            </p>
          </div>
          <button className={styles.closeBtn} onClick={onClose}>
            <X size={22} />
          </button>
        </div>

        <div className={styles.helpContent}>
          {/* Типы вопросов */}
          <section className={styles.helpSection}>
            <h3 className={styles.sectionTitle}>Типы вопросов</h3>
            <div className={styles.cardsGrid}>
              <div className={styles.helpCard}>
                <span className={`${styles.iconBox} ${styles.blue}`}>
                  <CheckCircle size={20} />
                </span>
                <div className={styles.cardBody}>
                  <p className={styles.cardTitle}>Один правильный ответ</p>
                  <p className={styles.cardDesc}>
                    Пользователь выбирает только один вариант (радио-кнопки).
                  </p>
                </div>
              </div>

              <div className={styles.helpCard}>
                <span className={`${styles.iconBox} ${styles.green}`}>
                  <ListChecks size={20} />
                </span>
                <div className={styles.cardBody}>
                  <p className={styles.cardTitle}>Несколько ответов</p>
                  <p className={styles.cardDesc}>
                    Можно выбрать несколько вариантов (чекбоксы). Баллы —
                    пропорционально верным.
                  </p>
                </div>
              </div>
            </div>
          </section>

          {/* Медиа файлы */}
          <section className={styles.helpSection}>
            <h3 className={styles.sectionTitle}>Медиа в вопросах</h3>
            <div className={styles.cardsGrid}>
              <div className={styles.helpCard}>
                <span className={`${styles.iconBox} ${styles.purple}`}>
                  <Image size={20} />
                </span>
                <div className={styles.cardBody}>
                  <p className={styles.cardTitle}>Изображения</p>
                  <p className={styles.cardDesc}>JPG, PNG, GIF — до 2 МБ</p>
                </div>
              </div>

              <div className={styles.helpCard}>
                <span className={`${styles.iconBox} ${styles.pink}`}>
                  <Video size={20} />
                </span>
                <div className={styles.cardBody}>
                  <p className={styles.cardTitle}>Видео</p>
                  <p className={styles.cardDesc}>MP4, WebM — до 10 МБ</p>
                </div>
              </div>

              <div className={styles.helpCard}>
                <span className={`${styles.iconBox} ${styles.orange}`}>
                  <Music size={20} />
                </span>
                <div className={styles.cardBody}>
                  <p className={styles.cardTitle}>Аудио</p>
                  <p className={styles.cardDesc}>MP3, WAV, OGG — до 5 МБ</p>
                </div>
              </div>
            </div>
          </section>

          {/* Система баллов */}
          <section className={styles.helpSection}>
            <h3 className={styles.sectionTitle}>Система баллов</h3>
            <div className={styles.scoreWrapper}>
              <p className={styles.scoreItem}>
                <strong>Одиночный выбор</strong> — полные баллы за верный ответ,
                0 за неверный.
              </p>
              <p className={styles.scoreItem}>
                <strong>Множественный выбор</strong> — баллы начисляются
                пропорционально:
              </p>
              <ul className={styles.scoreList}>
                <li>Все верные выбраны — 100% баллов</li>
                <li>2 из 3 верных — 67% (округление вниз)</li>
                <li>Выбран хотя бы 1 неверный — 0 баллов</li>
                <li>Ничего не выбрано — 0 баллов</li>
              </ul>
            </div>
          </section>

          {/* Примеры */}
          <section className={styles.helpSection}>
            <h3 className={styles.sectionTitle}>Примеры</h3>
            <div className={styles.examplesList}>
              <p>
                <span className={styles.exEmoji}>📸</span>
                <span>
                  <strong>С изображениями:</strong> «Угадай
                  достопримечательность по фото»
                </span>
              </p>
              <p>
                <span className={styles.exEmoji}>🎬</span>
                <span>
                  <strong>С видео:</strong> «Угадай фильм по отрывку»
                </span>
              </p>
              <p>
                <span className={styles.exEmoji}>🎵</span>
                <span>
                  <strong>С аудио:</strong> «Угадай песню или композитора»
                </span>
              </p>
              <p>
                <span className={styles.exEmoji}>✅</span>
                <span>
                  <strong>Множественный выбор:</strong> «Выберите все столицы
                  Европы»
                </span>
              </p>
            </div>
          </section>

          {/* Совет */}
          <div className={styles.tipBox}>
            💡 <strong>Совет:</strong> используйте файлы небольшого размера —
            так квиз загрузится быстрее у всех игроков.
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
