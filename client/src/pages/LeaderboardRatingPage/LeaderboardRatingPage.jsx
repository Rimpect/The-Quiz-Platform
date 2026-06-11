import { LeaderboardList } from '@entities'
import { ROUTES, Button, Badge } from '@shared'
import { Trophy } from 'lucide-react'
import { Link } from 'react-router-dom'

import styles from './LeaderboardPage.module.scss'

const mockData = [
  {
    place: 1,
    name: 'Team 1',
    avatar: 'https://i.pravatar.cc/150?img=1',
    percent: 90,
    time: '2:00',
  },
  {
    place: 2,
    name: 'Team 2',
    avatar: 'https://i.pravatar.cc/150?img=2',
    percent: 80,
    time: '2:00',
  },
  {
    place: 3,
    name: 'Team 3',
    avatar: 'https://i.pravatar.cc/150?img=3',
    percent: 70,
    time: '2:00',
  },
  {
    place: 4,
    name: 'Team 4',
    avatar: 'https://i.pravatar.cc/150?img=4',
    percent: 60,
    time: '2:00',
  },
  {
    place: 5,
    name: 'Team 5',
    avatar: 'https://i.pravatar.cc/150?img=5',
    percent: 50,
    time: '2:00',
  },
]

export function LeaderboardRatingPage() {
  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <div className={styles.title}>
          <Trophy size={32} color="blue" />
          <span>Таблица лидеров</span>
        </div>
        <div className={styles.badge}>
          <Badge size="medium" variant="team">
            {/* @TODO Добавить в Badge поддержку иконок */}
            Командный режим
          </Badge>
          <Link to={ROUTES.main}>
            <Button variant="white" size="medium">
              Назад к квизу
            </Button>
          </Link>
        </div>
      </div>
      <LeaderboardList items={mockData} />
    </div>
  )
}
