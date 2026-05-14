import { Calendar, Check, X } from 'lucide-react'

import styles from './StatsCards.module.scss'

export function StatsCards({ pendingCount, approvedCount, rejectedCount }) {
  const stats = [
    {
      label: 'На модерации',
      value: pendingCount,
      icon: Calendar,
      type: 'pending',
      iconBgColor: '#f8ef8b',
      iconColor: '#d97706',
    },
    {
      label: 'Одобрено',
      value: approvedCount,
      icon: Check,
      type: 'approved',
      iconBgColor: '#86eeaf',
      iconColor: '#16a34a',
    },
    {
      label: 'Отклонено',
      value: rejectedCount,
      icon: X,
      type: 'rejected',
      iconBgColor: '#fee2e2',
      iconColor: '#dc2626',
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
              <div
                className={styles.statIcon}
                style={{ backgroundColor: stat.iconBgColor }}
              >
                <IconComponent size={24} style={{ color: stat.iconColor }} />
              </div>
            </div>
          </div>
        )
      })}
    </div>
  )
}
