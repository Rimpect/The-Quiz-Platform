import { useEffect, useRef, useState } from 'react'

import { TeamCard, QuizInfoCard } from '@entities'
import { CreateTeamModal, useTimerSound } from '@features'
import { useGameLobby } from '@features/game-lobby/model/useGameLobby'
import { Button, ROUTES, Input } from '@shared'
import { Clock, Copy, Users } from 'lucide-react'
import { useNavigate, Link } from 'react-router-dom'
import { toast } from 'sonner'

import styles from './LobbyTeams.module.scss'

export function LobbyTeams({ quiz, quizId }) {
  const navigate = useNavigate()
  const startedRef = useRef(false)
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [codeInput, setCodeInput] = useState('')
  const [waitSeconds, setWaitSeconds] = useState(30)
  const WAIT_PRESETS = [15, 30, 60, 120, 300]
  const {
    sessionId,
    players,
    teams,
    lobbyStarted,
    lobbyTimeLeft,
    joinCode,
    cancelled,
    loading,
    myReady,
    myTeamId,
    markReady,
    createTeam,
    joinTeam,
    leaveTeam,
    createLobby,
    joinByCode,
    leaveLobby,
  } = useGameLobby(quizId, 'team')

  const leftRef = useRef(false)

  // Звук обратного отсчёта лобби: тиканье за 10 сек + звонок в конце
  useTimerSound(lobbyTimeLeft)

  // Когда лобби стартовало (все готовы или истёк общий таймер) — переходим к квизу
  useEffect(() => {
    if (lobbyStarted && !startedRef.current) {
      startedRef.current = true
      toast.success('Все готовы! Начинаем квиз...')
      navigate(`/quiz/${quizId}`, { state: { fromLobby: true, sessionId } })
    }
  }, [lobbyStarted, quizId, navigate, sessionId])

  // Хост вышел — лобби закрыто, всех выкидывает с ошибкой
  useEffect(() => {
    if (cancelled && !leftRef.current && !startedRef.current) {
      leftRef.current = true
      toast.error('Хост покинул лобби — оно закрыто')
      navigate(ROUTES.main, { replace: true })
    }
  }, [cancelled, navigate])

  const handleLeave = async () => {
    leftRef.current = true
    await leaveLobby()
    navigate(ROUTES.main, { replace: true })
  }

  const handleCreateTeam = (newTeam) => {
    createTeam(newTeam.name)
  }

  // Обратный отсчёт лобби: минуты:секунды, либо «N сек» при < 1 мин
  const formatCountdown = (s) =>
    s >= 60
      ? `${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')} мин`
      : `${s} сек`

  const copyCode = () => {
    navigator.clipboard?.writeText(joinCode).then(
      () => toast.success('Код скопирован'),
      () => {},
    )
  }

  // ----- Пре-лобби: создать своё лобби или войти по коду -----
  if (!sessionId) {
    return (
      <div className={styles.preLobby}>
        <div className={styles.preCard}>
          <Users size={40} className={styles.preIcon} />
          <h1>{quiz.title}</h1>
          <p className={styles.preHint}>Командный режим</p>

          <div className={styles.waitSetting}>
            <span className={styles.waitLabel}>
              <Clock size={16} /> Время ожидания игроков
            </span>
            <div className={styles.waitPresets}>
              {WAIT_PRESETS.map((sec) => (
                <button
                  key={sec}
                  type="button"
                  className={`${styles.waitPreset} ${
                    waitSeconds === sec ? styles.waitPresetActive : ''
                  }`}
                  onClick={() => setWaitSeconds(sec)}
                >
                  {sec < 60 ? `${sec} сек` : `${sec / 60} мин`}
                </button>
              ))}
            </div>
          </div>

          <Button
            variant="black"
            fullWidth
            onClick={() => createLobby(waitSeconds)}
            disabled={loading}
          >
            Создать лобби
          </Button>

          <div className={styles.preDivider}>или войдите по коду</div>

          <div className={styles.codeRow}>
            <Input
              type="text"
              placeholder="Код приглашения"
              value={codeInput}
              maxLength={6}
              onChange={(e) => setCodeInput(e.target.value.toUpperCase())}
            />
            <Button
              variant="green"
              onClick={() => joinByCode(codeInput)}
              disabled={loading || codeInput.trim().length < 4}
            >
              Войти
            </Button>
          </div>

          <Link to={ROUTES.main} className={styles.preBack}>
            Назад
          </Link>
        </div>
      </div>
    )
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
