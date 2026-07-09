import { IS_DEMO, FULL_VERSION_URL, REPO_URL } from '@shared'

import styles from './DemoBanner.module.scss'

export function DemoBanner() {
  if (!IS_DEMO) return null

  return (
    <div className={styles.banner}>
      <span className={styles.text}>
        Демо-версия со статичными данными. Полная версия с авторизацией и
        мультиплеером:
      </span>
      <a
        className={styles.link}
        href={FULL_VERSION_URL}
        target="_blank"
        rel="noopener noreferrer"
      >
        открыть полную версию
      </a>
      <span className={styles.sep}>·</span>
      <a
        className={styles.link}
        href={REPO_URL}
        target="_blank"
        rel="noopener noreferrer"
      >
        GitHub
      </a>
    </div>
  )
}
