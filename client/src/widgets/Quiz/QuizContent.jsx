import React, { useState, useEffect } from 'react'

import { useQuiz } from '@entities'
import {
  AnswerList,
  QuizProgress,
  QuizActions,
  QuestionSection,
  AnswerResult,
} from '@features'
import { useAntiCheatContext } from '@features/anti-cheating'
import { useNavigate, useLocation } from 'react-router-dom'

import { AntiCheatWarning } from './components/AntiCheatWarning'
import { QuizBlocked } from './components/QuizBlocked'
import { QuizError } from './components/QuizError'
import { QuizHeader } from './components/QuizHeader'
import { QuizLoading } from './components/QuizLoading'
import { useQuizLogic } from './hooks/useQuizLogic'
import styles from './Quiz.module.scss'

export const QuizContent = ({ quizId }) => {
  const navigate = useNavigate()
  const location = useLocation()
  const [showBlockedMessage, setShowBlockedMessage] = useState(false)
  const { violationsCount, isBlocked } = useAntiCheatContext()
  const { quiz, loading: quizLoading } = useQuiz(quizId)

  const {
    questions,
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
    toggleAnswer,
    handleTimeEnd,
    handleSubmitAnswer,
    handleNext,
  } = useQuizLogic(quizId)

  useEffect(() => {
    if (isBlocked) {
      setShowBlockedMessage(true)
    }
  }, [isBlocked])

  if (loading || quizLoading) return <QuizLoading />
  if (error) return <QuizError error={error} />
  if (!questions.length) return <QuizError error="Вопросы не найдены" />
  if (showBlockedMessage)
    return <QuizBlocked violationsCount={violationsCount} />

  return (
    <div className={styles.quizContainer}>
      <AntiCheatWarning violationsCount={violationsCount} />

      <QuizHeader
        title={quiz?.title}
        category={currentQ?.category}
        onTimeEnd={handleTimeEnd}
        timerKey={currentQuestion}
        timeLimitSeconds={currentQ?.timeLimitSeconds ?? null}
      />

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

      <QuizActions
        isAnswered={isAnswered}
        selectedAnswers={selectedAnswers}
        isLastQuestion={currentQuestion + 1 === totalQuestions}
        onSubmit={handleSubmitAnswer}
        onNext={handleNext}
      />
    </div>
  )
}
