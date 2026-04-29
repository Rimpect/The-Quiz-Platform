import { Calendar, Check, X } from 'lucide-react'
import styles from './StatsCards.module.scss'

export function StatsCards({ pendingCount, approvedCount, rejectedCount }) {
  const stats = [
    {
      label: 'На модерации',
      value: pendingCount,
      icon: Calendar,
      type: 'pending',
    },
    {
      label: 'Одобрено',
      value: approvedCount,
      icon: Check,
      type: 'approved',
    },
    {
      label: 'Отклонено',
      value: rejectedCount,
      icon: X,
      type: 'rejected',
    },
  ]

  return (
    <div className={styles.statsGrid}>
      {stats.map((stat) => {
        const IconComponent = stat.icon
        return (
          <div
            key={stat.type}
            className={`${styles.statCard} ${styles[stat.type]}`}
          >
            <div className={styles.statContent}>
              <div>
                <p className={styles.statLabel}>{stat.label}</p>
                <p className={styles.statValue}>{stat.value}</p>
              </div>
              <div className={styles.statIcon}>
                <IconComponent size={24} />{' '}
              </div>
            </div>
          </div>
        )
      })}
    </div>
  )
}
