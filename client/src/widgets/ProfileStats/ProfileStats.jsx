import {
  Trophy,
  Target,
  Clock,
  Award,
  Home,
  Settings as SettingsIcon,
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

  const levelProgress = ((user.xp || 0) / (user.nextLevelXp || 1)) * 100

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
                {(user.name || 'П').charAt(0)}
              </div>
            )}
          </div>

          <div className={styles.userInfo}>
            <div className={styles.nameSection}>
              <h1 className={styles.userName}>{user.name || 'Пользователь'}</h1>
              <span className={styles.levelBadge}>
                Уровень {user.level || 1}
              </span>
            </div>
            <p className={styles.userEmail}>
              {user.email || 'email@example.com'}
            </p>

            <div className={styles.xpSection}>
              <div className={styles.xpLabels}>
                <span>{user.xp || 0} XP</span>
                <span>{user.nextLevelXp || 1000} XP</span>
              </div>
              <div className={styles.progressBar}>
                <div
                  className={styles.progressFill}
                  style={{ width: `${levelProgress}%` }}
                />
              </div>
              <p className={styles.xpRemaining}>
                {(user.nextLevelXp || 1000) - (user.xp || 0)} XP до следующего
                уровня
              </p>
            </div>
          </div>

          <div className={styles.actionButtons}>
            <Link to="/MainPage">
              <button className={styles.btnOutline}>
                <Home size={16} />
                Главная
              </button>
            </Link>
            <Link to="/ProfileSettings">
              <button className={styles.btnOutline}>
                <SettingsIcon size={16} />
                Настройки
              </button>
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
