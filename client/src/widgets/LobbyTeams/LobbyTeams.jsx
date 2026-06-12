import { useEffect, useRef, useState } from 'react'

import { TeamCard, QuizInfoCard } from '@entities'
import { CreateTeamModal } from '@features'
import { useGameLobby } from '@features/game-lobby/model/useGameLobby'
import { Button, ROUTES } from '@shared'
import { Clock } from 'lucide-react'
import { useNavigate, Link } from 'react-router-dom'
import { toast } from 'sonner'

import styles from './LobbyTeams.module.scss'

export function LobbyTeams({ quiz, quizId }) {
  const navigate = useNavigate()
  const startedRef = useRef(false)
  const [isModalOpen, setIsModalOpen] = useState(false)
  const {
    sessionId,
    players,
    teams,
    lobbyStarted,
    lobbyTimeLeft,
    loading,
    myReady,
    myTeamId,
    markReady,
    createTeam,
    joinTeam,
    leaveTeam,
  } = useGameLobby(quizId, 'team')

  // Когда лобби стартовало (все готовы или истёк общий таймер) — переходим к квизу
  useEffect(() => {
    if (lobbyStarted && !startedRef.current) {
      startedRef.current = true
      toast.success('Все готовы! Начинаем квиз...')
      navigate(`/quiz/${quizId}`, { state: { fromLobby: true, sessionId } })
    }
  }, [lobbyStarted, quizId, navigate, sessionId])

  const handleCreateTeam = (newTeam) => {
    createTeam(newTeam.name)
  }

  // Маппинг команд с сервера в формат TeamCard
  const uiTeams = teams.map((t) => ({
    id: t.id,
    name: t.name,
    maxMembers: t.max_members,
    members: t.members.map((m) => ({
      id: m.user_id,
      name: m.nickname,
      isLeader: m.is_leader,
      isReady: m.is_ready,
    })),
  }))

  const myTeamName = uiTeams.find((t) => t.id === myTeamId)?.name

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h1>{quiz.title}</h1>
        <div className={styles.lobbyTimer}>
          <Clock size={20} />
          <span>
            {lobbyTimeLeft !== null
              ? `Старт через ${lobbyTimeLeft} сек`
              : 'Ожидание...'}
          </span>
        </div>
      </div>

      <div className={styles.content}>
        <div className={styles.teams}>
          <div className={styles.stats}>
            <span>
              Команды: {uiTeams.length} | Игроков: {players.length}
            </span>
            <Button
              variant="black"
              onClick={() => setIsModalOpen(true)}
              className={styles.createButton}
            >
              Создать команду
            </Button>
          </div>

          {loading && <div>Подключение к лобби...</div>}
          {!loading && uiTeams.length === 0 && (
            <div>Пока нет команд. Создайте первую!</div>
          )}

          {uiTeams.map((team) => (
            <TeamCard
              key={team.id}
              team={team}
              selectedTeam={myTeamId}
              onJoin={() => joinTeam(team.id)}
              onLeave={() => leaveTeam()}
            />
          ))}
        </div>

        <div className={styles.sidebar}>
          <QuizInfoCard quiz={quiz} />

          {myTeamId && (
            <div className={styles.readySection}>
              <p>
                Вы в команде <strong>{myTeamName}</strong>
              </p>
              <p>Нажмите "Готов", когда будете готовы начать</p>
              <Button variant="green" onClick={markReady} disabled={myReady}>
                {myReady ? 'Ожидаем остальных...' : 'Готов'}
              </Button>
            </div>
          )}

          <Link to={ROUTES.main}>
            <Button variant="white" fullWidth>
              Покинуть лобби
            </Button>
          </Link>
        </div>
      </div>

      <CreateTeamModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onCreate={handleCreateTeam}
      />
    </div>
  )
}
