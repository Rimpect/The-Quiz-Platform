import { useState } from 'react'

import { PlayerCard } from '@entities'
import { LobbyTimer } from '@features'
import { Button, ROUTES } from '@shared'
import { Trophy } from 'lucide-react'
import { Link } from 'react-router-dom'

import styles from './LobbyRating.module.scss'

export function LobbyRating({ quiz }) {
  const [players, setPlayers] = useState([
    {
      id: 1,
      name: 'Вы',
      avatar: '',
      isReady: false,
    },
    {
      id: 2,
      name: 'Максим',
      avatar: '',
      isReady: true,
    },
    {
      id: 3,
      name: 'Максим',
      avatar: '',
      isReady: true,
    },
    {
      id: 4,
      name: 'Максим',
      avatar: '',
      isReady: false,
    },
    {
      id: 5,
      name: 'Максим',
      avatar: '',
      isReady: true,
    },
  ])
  const currentPlayers = players.length
  const readyPlayers = players.filter((player) => player.isReady).length
  const updateReadyStatus = () => {
    setPlayers((prevPlayers) =>
      prevPlayers.map((player) =>
        player.id === 1 ? { ...player, isReady: !player.isReady } : player,
      ),
    )
  }

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <div className={styles.iconWrapper}>
          <Trophy size={24} color="#a855f7" />
        </div>
        <div>{quiz.title}</div>
        <div>Cоревновательный режим</div>
        <LobbyTimer
          initialTime={120}
          onTimeEnd={() => alert('Время вышло! Да начнутся игры!')}
        />
      </div>
      <div className={styles.playersInfo}>
        <div>Игроки {currentPlayers} </div>
        <div className={styles.playersReady}>
          {readyPlayers}/{currentPlayers} готовы
        </div>
      </div>
      <div className={styles.playersGrid}>
        {players.map((player) => (
          <PlayerCard
            key={player.id}
            player={player}
            isReady={player.isReady}
          />
        ))}
      </div>
      <div className={styles.quizInfo}>
        <div className={styles.section}>
          <div className={styles.info}>{quiz.questionCount}</div>
          <div>вопросов</div>
        </div>
        <div className={styles.section}>
          <div className={styles.info}>{quiz.duration}</div>
          <div>минут</div>
        </div>
        <div className={styles.section}>
          <div className={styles.info}>{quiz.difficulty}</div>
          <div>сложность</div>
        </div>
      </div>
      <div className={styles.actions}>
        <Link to={ROUTES.main}>
          <Button fullWidth>кнопка покинуть лобби</Button>
        </Link>
        {/* @TODO пока что хардкод с id игрока что бы проверить на работоспособность */}
        <Button fullWidth onClick={updateReadyStatus}>
          {players.find((p) => p.id === 1)?.isReady
            ? 'Отменить готовность'
            : 'Готов к игре'}
        </Button>
      </div>
    </div>
  )
}
