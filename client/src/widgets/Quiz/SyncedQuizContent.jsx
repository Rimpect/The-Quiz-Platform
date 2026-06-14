import React, { useEffect } from 'react'

import {
  AnswerList,
  QuizProgress,
  QuestionSection,
  AnswerResult,
  QuizTimer,
  useTimerSound,
} from '@features'
import { useAntiCheatContext } from '@features/anti-cheating'
import { useSyncedQuiz } from '@features/synced-quiz'
import { Button, ROUTES } from '@shared'
import { client } from '@shared/api/client'
import { Users } from 'lucide-react'
import { Link, useNavigate } from 'react-router-dom'

import { AntiCheatWarning } from './components/AntiCheatWarning'
import { PlayersStatus } from './components/PlayersStatus'
import { QuizBlocked } from './components/QuizBlocked'
import { QuizError } from './components/QuizError'
import { QuizLoading } from './components/QuizLoading'
import styles from './Quiz.module.scss'

export const SyncedQuizContent = ({ quizId, sessionId }) => {
  const { violationsCount, isBlocked } = useAntiCheatContext()
  const navigate = useNavigate()

  // Бан — per-player: сообщаем серверу, остальные (и хост) продолжают
  useEffect(() => {
    if (isBlocked && sessionId) {
      client(`/game/sessions/${sessionId}/banned`, { method: 'POST' }).catch(
        () => {},
      )
    }
  }, [isBlocked, sessionId])

  const {
    currentQ,
    currentQuestion,
    totalQuestions,
    isAnswered,
    loading,
    error,
    selectedAnswers,
    currentScore,
    totalScore,
    maxPossibleScore,
    timeLeft,
    toggleAnswer,
    submitAnswer,
    isTeam,
    isLeader,
    voters,
    hasVoted,
    leaderAnswered,
    meBanned,
    players,
    teams,
  } = useSyncedQuiz(quizId, sessionId)

  // Звук таймера вопроса (серверное время): предупреждение + «звонок» в конце
  useTimerSound(timeLeft)

  // Рядовой участник команды (не капитан): только голосует
  const isVoter = isTeam && !isLeader
  const voteLocked = leaderAnswered || timeLeft === 0

  // Блокировка: локальный анти-чит ИЛИ серверный бан (переживает перезагрузку)
  const blocked = isBlocked || meBanned

  // С экрана бана авто-редирект на главную (и чистим сохранённую сессию),
  // чтобы забаненный не мог вернуться в квиз сворачиванием/перезагрузкой
  useEffect(() => {
    if (!blocked) return
    const t = setTimeout(() => {
      try {
        sessionStorage.removeItem(`quizSession:${quizId}`)
      } catch {
        // no-op
      }
      navigate(ROUTES.main, { replace: true })
    }, 5000)
    return () => clearTimeout(t)
  }, [blocked, quizId, navigate])

  if (blocked)
    return <QuizBlocked violationsCount={Math.max(violationsCount, 3)} />
  if (loading) return <QuizLoading />
  if (error) return <QuizError error={error} />
  if (!currentQ) return <QuizLoading />

  return (
    <div className={styles.quizContainer}>
      <AntiCheatWarning violationsCount={violationsCount} />

      <div className={styles.quizHeader}>
        <div className={styles.quizInfo}>
          <Link to={ROUTES.main} className={styles.exitLink}>
            Выход
          </Link>
          <div className={styles.quizCategory}>
            <Users size={16} />{' '}
            {isTeam
              ? isLeader
                ? 'Капитан команды'
                : 'Голосование в команде'
              : 'Совместный режим'}
          </div>
        </div>
        <QuizTimer timeLeft={timeLeft} />
      </div>

      <QuizProgress
        currentQuestion={currentQuestion}
        totalQuestions={totalQuestions}
        totalScore={totalScore}
        maxPossibleScore={maxPossibleScore}
      />

      {isTeam && <PlayersStatus players={players} teams={teams} />}

      <div className={styles.questionContainer}>
        <QuestionSection question={currentQ} />
        <AnswerList
          options={currentQ?.options}
          selectedAnswers={selectedAnswers}
          correctAnswers={currentQ?.correctAnswers}
          questionType={currentQ?.questionType}
          isAnswered={isAnswered}
          onSelect={
            isAnswered || (isVoter && voteLocked) ? () => {} : toggleAnswer
          }
          voters={isTeam ? voters : undefined}
        />
        <AnswerResult
          isAnswered={isAnswered}
          score={currentScore}
          points={currentQ?.points}
        />
      </div>

      {isVoter ? (
        // ----- Рядовой участник команды: только голос -----
        voteLocked ? (
          <div className={styles.waitingNext}>
            Капитан зафиксировал ответ команды. Переходим дальше...
          </div>
        ) : (
          <>
            <Button
              variant="green"
              fullWidth
              onClick={submitAnswer}
              disabled={selectedAnswers.length === 0}
            >
              {hasVoted ? 'Изменить голос' : 'Голосовать'}
            </Button>
            <div className={styles.voteHint}>
              Решение принимает капитан. Ваш голос виден команде.
            </div>
          </>
        )
      ) : isAnswered ? (
        <div className={styles.waitingNext}>
          {isTeam
            ? 'Ответ команды зафиксирован. Ждём остальных капитанов...'
            : 'Ответ принят. Ждём остальных и переход к следующему вопросу...'}
        </div>
      ) : (
        <Button
          variant="green"
          fullWidth
          onClick={submitAnswer}
          disabled={selectedAnswers.length === 0}
        >
          {isTeam ? 'Ответить за команду' : 'Ответить'}
        </Button>
      )}
    </div>
  )
}
