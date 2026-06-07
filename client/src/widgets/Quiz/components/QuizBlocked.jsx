import { ROUTES } from '@shared'
import { Link } from 'react-router-dom'

import styles from '../Quiz.module.scss'

export const QuizBlocked = ({ violationsCount }) => {
  return (
    <div className={styles.blockedContainer}>
      <div className={styles.blockedCard}>
        <span className={styles.blockedIcon}>🚫</span>
        <h2>Квиз заблокирован!</h2>
        <p>Вы получили {violationsCount} предупреждения за нарушение правил.</p>
        <p className={styles.blockedReason}>Причины блокировки:</p>
        <ul className={styles.blockedList}>
          <li>🚫 Переключение вкладок</li>
          <li>🚫 Копирование и вставка</li>
          <li>🚫 Открытие инструментов разработчика</li>
        </ul>
        <Link to={ROUTES.main} className={styles.backButton}>
          Вернуться на главную
        </Link>
      </div>
    </div>
  )
}
