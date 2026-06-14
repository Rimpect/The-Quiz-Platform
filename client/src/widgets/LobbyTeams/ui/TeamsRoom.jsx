import { useState } from 'react'

import { TeamCard, QuizInfoCard } from '@entities'
import { CreateTeamModal } from '@features'
import { Button } from '@shared'
import { Clock, Copy } from 'lucide-react'
import { toast } from 'sonner'

import styles from '../LobbyTeams.module.scss'

// Обратный отсчёт лобби: минуты:секунды, либо «N сек» при < 1 мин
const formatCountdown = (s) =>
  s >= 60
    ? `${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')} мин`
    : `${s} сек`

// Маппинг команд с сервера в формат TeamCard
const toUiTeams = (teams) =>
  teams.map((t) => ({
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

/**
 * Основной экран лобби: список команд, информация о квизе, готовность и выход.
 */
export function TeamsRoom({ quiz, lobby }) {
  const {
    players,
    teams,
    joinCode,
    lobbyTimeLeft,
    myReady,
    myTeamId,
    loading,
    markReady,
    joinTeam,
    leaveTeam,
    handleLeave,
    handleCreateTeam,
  } = lobby

  const [isModalOpen, setIsModalOpen] = useState(false)

  const uiTeams = toUiTeams(teams)
  const myTeamName = uiTeams.find((t) => t.id === myTeamId)?.name

  const copyCode = () => {
    navigator.clipboard?.writeText(joinCode).then(
      () => toast.success('Код скопирован'),
      () => {},
    )
  }

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h1>{quiz.title}</h1>
        <div className={styles.headerRight}>
          {joinCode && (
            <button
              type="button"
              className={styles.codeBadge}
              onClick={copyCode}
            >
              Код: <strong>{joinCode}</strong>
              <Copy size={16} />
            </button>
          )}
          <div className={styles.lobbyTimer}>
            <Clock size={20} />
            <span>
              {lobbyTimeLeft !== null
                ? `Старт через ${formatCountdown(lobbyTimeLeft)}`
                : 'Ожидание...'}
            </span>
          </div>
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
              disabled={!!myTeamId}
              title={
                myTeamId
                  ? 'Сначала покиньте текущую команду'
                  : 'Создать новую команду'
              }
            >
              Создать команду
            </Button>
          </div>

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

          <Button variant="white" fullWidth onClick={handleLeave}>
            Покинуть лобби
          </Button>
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
