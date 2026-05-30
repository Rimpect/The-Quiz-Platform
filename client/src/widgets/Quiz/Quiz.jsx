// Quiz.jsx
import React, { useState } from 'react'

import { mockDataQuestions } from '@entities'
import {
  QuizTimer,
  AnswerList,
  QuizProgress,
  QuizActions,
  QuestionSection,
  AnswerResult,
  calculatePartialScore,
  useAnswerSelection,
  checkAnswer,
} from '@features'
import { ROUTES } from '@shared'
import { Link, useParams, useNavigate } from 'react-router-dom'

import styles from './Quiz.module.scss'

export function Quiz() {
  const { id } = useParams()
  const [currentQuestion, setCurrentQuestion] = useState(0)
  const [isAnswered, setIsAnswered] = useState(false)
  const [totalScore, setTotalScore] = useState(0)
  const [correctCount, setCorrectCount] = useState(0)
  const [isFinished, setIsFinished] = useState(false)
  const navigate = useNavigate()
  const questions = mockDataQuestions

  const totalQuestions = questions.length
  const currentQ = questions[currentQuestion]

  const { selectedAnswers, toggleAnswer, resetAnswers } = useAnswerSelection(
    currentQ.questionType,
  )
  const currentScore = calculatePartialScore(
    selectedAnswers,
    currentQ.correctAnswers,
    currentQ.points,
  )

  const maxPossibleScore = questions.reduce((sum, q) => sum + q.points, 0)

  const handleTimeEnd = () => {
    if (isAnswered) return

    handleSubmitAnswer()
    handleNext()
  }
  const handleSubmitAnswer = () => {
    setIsAnswered(true)

    const earnedPoints = currentScore
    setTotalScore((prev) => prev + earnedPoints)
    const isFullyCorrect = checkAnswer(selectedAnswers, currentQ.correctAnswers)
    if (isFullyCorrect) {
      setCorrectCount((prev) => prev + 1)
    }
  }

  const handleNext = () => {
    if (currentQuestion + 1 < totalQuestions) {
      setCurrentQuestion((prev) => prev + 1)
      resetAnswers()
      setIsAnswered(false)
    } else {
      setIsFinished(true)
    }
  }

  if (isFinished) {
    const percentScore = Math.round((totalScore / maxPossibleScore) * 100)
    navigate(ROUTES.finishQuiz, {
      state: {
        totalScore,
        maxPossibleScore,
        percentScore,
        correctCount,
        totalQuestions,
      },
    })

    return null
  }

  return (
    <div className={styles.quizContainer}>
      <div className={styles.quizHeader}>
        <div className={styles.quizInfo}>
          <Link to={ROUTES.main} className={styles.quizId}>
            Выход
          </Link>

          <div className={styles.quizCategory}>
            {currentQ.category || 'Общий'}
          </div>
        </div>

        <QuizTimer
          key={currentQuestion}
          duration={5}
          // warningSound={warningSound}
          onTimeEnd={handleTimeEnd}
        />
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
          options={currentQ.options}
          selectedAnswers={selectedAnswers}
          correctAnswers={currentQ.correctAnswers}
          questionType={currentQ.questionType}
          isAnswered={isAnswered}
          onSelect={toggleAnswer}
        />
        <AnswerResult
          isAnswered={isAnswered}
          score={currentScore}
          points={currentQ.points}
        />
      </div>

      <QuizActions
        isAnswered={isAnswered}
        selectedAnswers={selectedAnswers}
        isLastQuestion={currentQuestion + 1 === totalQuestions}
        onSubmit={handleSubmitAnswer}
        onNext={handleNext}
      />

      <div className={styles.leaderboardPreview}>
        <h3>Таблица лидеров</h3>
        <p>Места участников в данный момент</p>
        <div className={styles.leaderboardPlaceholder}>
          {/* Здесь будет таблица лидеров */}
        </div>
      </div>
    </div>
  )
}
