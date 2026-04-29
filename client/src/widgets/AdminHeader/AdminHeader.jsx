import styles from './AdminHeader.module.scss'

export function AdminHeader({ onBack }) {
  return (
    <div className={styles.header}>
      <div className={styles.headerContent}>
        <div>
          <div className={styles.titleWrapper}>
            <span className={styles.shieldIcon}>🛡️</span>
            <h1 className={styles.title}>Админ-панель</h1>
          </div>
          <p className={styles.subtitle}>
            Управление квизами и модерация контента
          </p>
        </div>
        <button className={styles.backButton} onClick={onBack}>
          Назад
        </button>
      </div>
    </div>
  )
}
