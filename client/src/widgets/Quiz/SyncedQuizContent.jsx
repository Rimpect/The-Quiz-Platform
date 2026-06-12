import React, { useEffect, useState } from 'react'

import {
  AnswerList,
  QuizProgress,
  QuestionSection,
  AnswerResult,
} from '@features'
import { useAntiCheatContext } from '@features/anti-cheating'
import { useSyncedQuiz } from '@features/synced-quiz/model/useSyncedQuiz'
import { Button, ROUTES } from '@shared'
import { Clock, Users } from 'lucide-react'
import { Link } from 'react-router-dom'

import { AntiCheatWarning } from './components/AntiCheatWarning'
import { QuizBlocked } from './components/QuizBlocked'
import { QuizError } from './components/QuizError'
import { QuizLoading } from './components/QuizLoading'
import styles from './Quiz.module.scss'

export const SyncedQuizContent = ({ quizId, sessionId }) => {
  const { violationsCount, isBlocked } = useAntiCheatContext()
  const [showBlockedMessage, setShowBlockedMessage] = useState(false)

  useEffect(() => {
    if (isBlocked) setShowBlockedMessage(true)
  }, [isBlocked])

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
  } = useSyncedQuiz(quizId, sessionId)

  if (showBlockedMessage)
    return <QuizBlocked violationsCount={violationsCount} />
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
            <Users size={16} /> Совместный режим
          </div>
        </div>
        <div className={styles.syncedTimer}>
          <Clock size={20} />
          <span>{timeLeft !== null ? `${timeLeft} сек` : '—'}</span>
        </div>
      </div>

      <QuizProgress
        currentQuestion={currentQuestion}
        totalQuestions={totalQuestions}
        totalScore={totalScore}
        maxPossibleScore={maxPossibleScore}
      />

      <div className={styles.questionContainer}>
        <QuestionSection question={currentQ} />
        <AnswerList
          options={currentQ?.options}
          selectedAnswers={selectedAnswers}
          correctAnswers={currentQ?.correctAnswers}
          questionType={currentQ?.questionType}
          isAnswered={isAnswered}
          onSelect={toggleAnswer}
        />
        <AnswerResult
          isAnswered={isAnswered}
          score={currentScore}
          points={currentQ?.points}
        />
      </div>

      {isAnswered ? (
        <div className={styles.waitingNext}>
          Ответ принят. Ждём остальных и переход к следующему вопросу...
        </div>
      ) : (
        <Button
          variant="green"
          fullWidth
          onClick={submitAnswer}
          disabled={selectedAnswers.length === 0}
        >
          Ответить
        </Button>
      )}
    </div>
  )
}
