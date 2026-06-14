import { useEffect, useRef } from 'react'

import { PlayerCard } from '@entities'
import { useTimerSound } from '@features'
import { useGameLobby } from '@features/game-lobby/model/useGameLobby'
import { Button, ROUTES } from '@shared'
import { Trophy, Clock } from 'lucide-react'
import { Link, useNavigate } from 'react-router-dom'
import { toast } from 'sonner'

import styles from './LobbyRating.module.scss'

export function LobbyRating({ quiz, quizId }) {
  const navigate = useNavigate()
  const startedRef = useRef(false)
  const {
    sessionId,
    players,
    lobbyStarted,
    lobbyTimeLeft,
    loading,
    myReady,
    readyCount,
    markReady,
  } = useGameLobby(quizId, 'competitive')

  // Звук обратного отсчёта лобби: тиканье за 10 сек + звонок в конце
  useTimerSound(lobbyTimeLeft)

  // Когда лобби стартовало (все готовы или истёк общий таймер) — переходим к квизу
  useEffect(() => {
    if (lobbyStarted && !startedRef.current) {
      startedRef.current = true
      toast.success('Начинаем квиз!')
      navigate(`/quiz/${quizId}`, { state: { fromLobby: true, sessionId } })
    }
  }, [lobbyStarted, quizId, navigate, sessionId])

  const uiPlayers = players.map((p) => ({
    id: p.user_id,
    name: p.nickname,
    avatar: p.photo_profile || '',
    isReady: p.is_ready,
  }))

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <div className={styles.iconWrapper}>
          <Trophy size={24} color="#a855f7" />
        </div>
        <div>{quiz.title}</div>
        <div>Cоревновательный режим</div>
        <div className={styles.lobbyTimer}>
          <Clock size={20} />
          <span>
            {lobbyTimeLeft !== null
              ? `Старт через ${lobbyTimeLeft} сек`
              : 'Ожидание...'}
          </span>
        </div>
      </div>
      <div className={styles.playersInfo}>
        <div>Игроки {uiPlayers.length} </div>
        <div className={styles.playersReady}>
          {readyCount}/{uiPlayers.length} готовы
        </div>
      </div>
      <div className={styles.playersGrid}>
        {loading && <div>Подключение к лобби...</div>}
        {uiPlayers.map((player) => (
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
          <Button fullWidth>Покинуть лобби</Button>
        </Link>
        <Button fullWidth onClick={markReady} disabled={myReady}>
          {myReady ? 'Ожидаем остальных...' : 'Готов к игре'}
        </Button>
      </div>
    </div>
  )
}
