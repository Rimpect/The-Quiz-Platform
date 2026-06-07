import React, { useState, useEffect } from 'react'

import {
  AnswerList,
  QuizProgress,
  QuizActions,
  QuestionSection,
  AnswerResult,
} from '@features'
import { useAntiCheatContext } from '@features/anti-cheating'

import { AntiCheatWarning } from './components/AntiCheatWarning'
import { QuizBlocked } from './components/QuizBlocked'
import { QuizError } from './components/QuizError'
import { QuizHeader } from './components/QuizHeader'
import { QuizLoading } from './components/QuizLoading'
import { useQuizLogic } from './hooks/useQuizLogic'
import styles from './Quiz.module.scss'

export const QuizContent = ({ quizId }) => {
  const [showBlockedMessage, setShowBlockedMessage] = useState(false)
  const { violationsCount, isBlocked } = useAntiCheatContext()

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

  if (loading) return <QuizLoading />
  if (error) return <QuizError error={error} />
  if (!questions.length) return <QuizError error="Вопросы не найдены" />
  if (showBlockedMessage)
    return <QuizBlocked violationsCount={violationsCount} />

  return (
    <div className={styles.quizContainer}>
      <AntiCheatWarning violationsCount={violationsCount} />

      <QuizHeader
        category={currentQ?.category}
        onTimeEnd={handleTimeEnd}
        timerKey={currentQuestion}
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
