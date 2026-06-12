import { useState } from 'react'

import { LeaderboardList } from '@entities'
import { useLeaderboard } from '@entities/leaderboard/model/useLeaderboard'
import { useSessionResults } from '@entities/leaderboard/model/useSessionResults'
import { ROUTES, Button, Badge } from '@shared'
import { Trophy, Users } from 'lucide-react'
import { useParams, useLocation, Link } from 'react-router-dom'

import styles from './LeaderboardPage.module.scss'

const MODE_CONFIG = {
  team: {
    badge: 'Командный',
    variant: 'team',
    icon: Users,
    iconColor: '#22c55e',
  },
  competitive: {
    badge: 'Рейтинг',
    variant: 'competitive',
    icon: Trophy,
    iconColor: '#a855f7',
  },
}

export function LeaderboardRatingPage() {
  const { quizId } = useParams()
  const { state } = useLocation()
  const sessionId = state?.sessionId || null

  const {
    leaderboard,
    loading: gLoading,
    error: gError,
  } = useLeaderboard(Number(quizId))
  const {
    results,
    loading: sLoading,
    error: sError,
  } = useSessionResults(sessionId)

  // Если пришли с сессии — по умолчанию показываем результаты группы
  const [view, setView] = useState(sessionId ? 'session' : 'global')

  const mode = state?.quizMode === 'team' ? 'team' : 'competitive'
  const config = MODE_CONFIG[mode]
  const Icon = config.icon

  const isSession = view === 'session'
  const items = isSession ? results : leaderboard
  const loading = isSession ? sLoading : gLoading
  const error = isSession ? sError : gError
  const title = isSession
    ? 'Результаты группы'
    : 'Таблица лидеров (общий рейтинг)'

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <div className={styles.title}>
          <Icon size={32} color={config.iconColor} />
          <span>{title}</span>
        </div>
        <div className={styles.badge}>
          <Badge size="medium" variant={config.variant}>
            {config.badge}
          </Badge>
          <Link to={ROUTES.main}>
            <Button variant="white" size="medium">
              Назад к квизам
            </Button>
          </Link>
        </div>
      </div>

      {sessionId && (
        <div className={styles.tabs}>
          <Button
            variant={isSession ? 'black' : 'white'}
            size="medium"
            onClick={() => setView('session')}
          >
            Результаты группы
          </Button>
          <Button
            variant={!isSession ? 'black' : 'white'}
            size="medium"
            onClick={() => setView('global')}
          >
            Общий рейтинг
          </Button>
        </div>
      )}

      {loading && (
        <div style={{ padding: '2rem', textAlign: 'center' }}>Загрузка...</div>
      )}
      {error && <div style={{ padding: '2rem', color: 'red' }}>{error}</div>}
      {!loading && items.length === 0 && (
        <div style={{ padding: '2rem', textAlign: 'center', color: '#666' }}>
          Нет данных для отображения
        </div>
      )}
      {!loading && items.length > 0 && <LeaderboardList items={items} />}
    </div>
  )
}
