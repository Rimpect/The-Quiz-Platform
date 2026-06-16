import { Button, ROUTES } from '@shared'
import {
  Trophy,
  Target,
  Clock,
  Award,
  Home,
  Settings as SettingsIcon,
  User,
} from 'lucide-react'
import { Link } from 'react-router-dom'

import styles from './ProfileStats.module.scss'

export function ProfileStats({ user }) {
  if (!user) {
    return (
      <div className={styles.profileCard}>
        <div className={styles.profileHeader}>
          <div className={styles.loadingState}>
            <p>Загрузка данных пользователя...</p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className={styles.profileCard}>
      <div className={styles.profileHeader}>
        <div className={styles.headerTop}>
          <div className={styles.avatar}>
            {user.avatar ? (
              <img
                src={user.avatar}
                alt={user.name || 'User'}
                className={styles.avatarImage}
              />
            ) : (
              <div className={styles.avatarFallback}>
                <User size={40} />
              </div>
            )}
          </div>

          <div className={styles.userInfo}>
            <div className={styles.nameSection}>
              <h1 className={styles.userName}>{user.name || 'Пользователь'}</h1>
            </div>
          </div>

          <div className={styles.actionButtons}>
            <Link to={ROUTES.main}>
              <Button variant="white" size="medium" icon={<Home size={20} />}>
                Главная
              </Button>
            </Link>
            <Link to={ROUTES.settings}>
              <Button
                variant="white"
                size="medium"
                icon={<SettingsIcon size={20} />}
              >
                Настройки
              </Button>
            </Link>
          </div>
        </div>

        <div className={styles.statsGrid}>
          <div className={styles.statItem}>
            <Trophy className={`${styles.statIcon} ${styles.trophyIcon}`} />
            <div className={styles.statValue}>{user.totalQuizzes || 0}</div>
            <div className={styles.statLabel}>Квизов пройдено</div>
          </div>
          <div className={styles.statItem}>
            <Target className={`${styles.statIcon} ${styles.targetIcon}`} />
            <div className={styles.statValue}>{user.averageScore || 0}%</div>
            <div className={styles.statLabel}>Средний балл</div>
          </div>
          <div className={styles.statItem}>
            <Award className={`${styles.statIcon} ${styles.awardIcon}`} />
            <div className={styles.statValue}>{user.bestScore || 0}%</div>
            <div className={styles.statLabel}>Лучший результат</div>
          </div>
          <div className={styles.statItem}>
            <Clock className={`${styles.statIcon} ${styles.clockIcon}`} />
            <div className={styles.statValue}>{user.totalTime || 0}</div>
            <div className={styles.statLabel}>Минут в игре</div>
          </div>
        </div>
      </div>
    </div>
  )
}
