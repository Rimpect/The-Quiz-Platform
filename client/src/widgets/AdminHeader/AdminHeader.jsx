import { Shield } from 'lucide-react'
import { Link } from 'react-router-dom'
import styles from './AdminHeader.module.scss'

export function AdminHeader() {
  return (
    <div className={styles.header}>
      <div className={styles.headerContent}>
        <div>
          <div className={styles.titleWrapper}>
            <span className={styles.shieldIcon}>
              <Shield color="#1d4ed8" size={26} />
            </span>
            <h1 className={styles.title}>Админ-панель</h1>
          </div>
          <p className={styles.subtitle}>
            Управление квизами и модерация контента
          </p>
        </div>

        <Link to="/MainPage" className={styles.backButton}>
          <span>Назад</span>
        </Link>
      </div>
    </div>
  )
}
