// Quiz.jsx
import React, { useState, useEffect } from 'react'

import { QuizTimer, AnswerList, QuizProgress, QuizActions } from '@features'
import { ROUTES } from '@shared'
import { Link, useParams, useNavigate } from 'react-router-dom'

import styles from './Quiz.module.scss'

export function Quiz() {
  const { id } = useParams()
  const [currentQuestion, setCurrentQuestion] = useState(0)
  const [selectedAnswers, setSelectedAnswers] = useState([])
  const [isAnswered, setIsAnswered] = useState(false)
  const [totalScore, setTotalScore] = useState(0)
  const [maxPossibleScore, setMaxPossibleScore] = useState(0)
  const [correctCount, setCorrectCount] = useState(0)
  const [isFinished, setIsFinished] = useState(false)

  const navigate = useNavigate()

  // Расширенные вопросы с поддержкой разных типов и медиа
  const questions = [
    {
      id: '1',
      question: 'Что изображено на этой картине?',
      questionType: 'single',
      mediaType: 'image',
      mediaUrl:
        'https://images.unsplash.com/photo-1770301380828-3ebc4a260d34?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxmYW1vdXMlMjBwYWludGluZyUyMGFydCUyMG1hc3RlcnBpZWNlfGVufDF8fHx8MTc3MjUzMTY1N3ww&ixlib=rb-4.1.0&q=80&w=1080',
      options: ['Пейзаж', 'Портрет', 'Натюрморт', 'Абстракция'],
      correctAnswers: [0],
      points: 10,
    },
    {
      id: '2',
      question: 'Какая планета является самой большой в Солнечной системе?',
      questionType: 'single',
      options: ['Марс', 'Сатурн', 'Юпитер', 'Нептун'],
      correctAnswers: [2],
      points: 10,
    },
    {
      id: '3',
      question: 'Выберите все столицы европейских стран:',
      questionType: 'multiple',
      options: ['Париж', 'Токио', 'Берлин', 'Пекин'],
      correctAnswers: [0, 2],
      points: 15,
    },
    {
      id: '4',
      question: 'Какие инструменты относятся к струнным?',
      questionType: 'multiple',
      mediaType: 'image',
      mediaUrl:
        'https://images.unsplash.com/photo-1769942788839-69f12fbd60ab?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxtdXNpY2FsJTIwaW5zdHJ1bWVudHMlMjBvcmNoZXN0cmF8ZW58MXx8fHwxNzcyNTMxNjU3fDA&ixlib=rb-4.1.0&q=80&w=1080',
      options: ['Скрипка', 'Труба', 'Гитара', 'Барабан'],
      correctAnswers: [0, 2],
      points: 15,
    },
    {
      id: '5',
      question: 'Выберите все планеты земной группы:',
      questionType: 'multiple',
      options: ['Марс', 'Юпитер', 'Венера', 'Сатурн'],
      correctAnswers: [0, 2],
      points: 15,
    },
    {
      id: '6',
      question: 'В каком году началась Вторая мировая война?',
      questionType: 'single',
      options: ['1937', '1939', '1941', '1945'],
      correctAnswers: [1],
      points: 10,
    },
    {
      id: '7',
      question: 'Выберите произведения Льва Толстого:',
      questionType: 'multiple',
      options: [
        'Война и мир',
        'Преступление и наказание',
        'Анна Каренина',
        'Мертвые души',
      ],
      correctAnswers: [0, 2],
      points: 15,
    },
    {
      id: '8',
      question: 'Что вы видите на этом изображении?',
      questionType: 'single',
      mediaType: 'image',
      mediaUrl:
        'https://images.unsplash.com/photo-1600257729950-13a634d32697?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxuYXR1cmUlMjBsYW5kc2NhcGUlMjBtb3VudGFpbnN8ZW58MXx8fHwxNzcyNDEwMzI2fDA&ixlib=rb-4.1.0&q=80&w=1080',
      options: ['Океан', 'Пустыня', 'Горы', 'Лес'],
      correctAnswers: [2],
      points: 10,
    },
    {
      id: '9',
      question: 'Выберите языки программирования:',
      questionType: 'multiple',
      options: ['Python', 'HTML', 'JavaScript', 'CSS'],
      correctAnswers: [0, 2],
      points: 15,
    },
    {
      id: '10',
      question: 'Какая самая длинная река в мире?',
      questionType: 'single',
      options: ['Амазонка', 'Нил', 'Янцзы', 'Миссисипи'],
      correctAnswers: [1],
      points: 10,
    },
  ]

  const totalQuestions = questions.length
  const currentQ = questions[currentQuestion]

  // Вычисляем максимально возможный балл
  useEffect(() => {
    const maxScore = questions.reduce((sum, q) => sum + q.points, 0)
    setMaxPossibleScore(maxScore)
  }, [])

  const toggleAnswer = (index) => {
    if (isAnswered) return

    if (currentQ.questionType === 'single') {
      setSelectedAnswers([index])
    } else {
      // Множественный выбор
      const newAnswers = [...selectedAnswers]
      const answerIndex = newAnswers.indexOf(index)
      if (answerIndex > -1) {
        newAnswers.splice(answerIndex, 1)
      } else {
        newAnswers.push(index)
      }
      setSelectedAnswers(newAnswers.sort((a, b) => a - b))
    }
  }

  const calculatePartialScore = () => {
    if (selectedAnswers.length === 0) return 0

    const correctSet = new Set(currentQ.correctAnswers)

    // Подсчитываем правильные и неправильные выборы
    let correctSelected = 0
    let incorrectSelected = 0

    selectedAnswers.forEach((answer) => {
      if (correctSet.has(answer)) {
        correctSelected++
      } else {
        incorrectSelected++
      }
    })

    // Если есть неправильные выборы, баллы не начисляются
    if (incorrectSelected > 0) {
      return 0
    }

    // Частичные баллы: пропорционально выбранным правильным ответам
    const percentageCorrect = correctSelected / currentQ.correctAnswers.length
    return Math.floor(currentQ.points * percentageCorrect)
  }

  const handleSubmitAnswer = () => {
    setIsAnswered(true)

    const earnedPoints = calculatePartialScore()
    setTotalScore(totalScore + earnedPoints)

    // Считаем полностью правильный ответ
    const isFullyCorrect =
      selectedAnswers.length === currentQ.correctAnswers.length &&
      selectedAnswers.every((ans, i) => ans === currentQ.correctAnswers[i])

    if (isFullyCorrect) {
      setCorrectCount(correctCount + 1)
    }
  }

  const handleNext = () => {
    if (currentQuestion + 1 < totalQuestions) {
      setCurrentQuestion(currentQuestion + 1)
      setSelectedAnswers([])
      setIsAnswered(false)
    } else {
      // Квиз завершен
      setIsFinished(true)
    }
  }

  const getOptionClassName = (index) => {
    if (!isAnswered) {
      const isSelected = selectedAnswers.includes(index)
      return `${styles.answerOption} ${isSelected ? styles.selected : ''}`
    }

    const isCorrect = currentQ.correctAnswers.includes(index)
    const isSelected = selectedAnswers.includes(index)

    if (isCorrect) {
      return `${styles.answerOption} ${styles.correct}`
    }
    if (isSelected && !isCorrect) {
      return `${styles.answerOption} ${styles.incorrect}`
    }
    return `${styles.answerOption} ${styles.disabled}`
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
          duration={30}
          // warningSound={warningSound}
          onTimeEnd={() => {
            console.log('Время вышло')
          }}
        />
      </div>
      <QuizProgress
        currentQuestion={currentQuestion}
        totalQuestions={totalQuestions}
        totalScore={totalScore}
        maxPossibleScore={maxPossibleScore}
      />

      <div className={styles.questionContainer}>
        {currentQ.mediaUrl && (
          <div className={styles.mediaContainer}>
            {currentQ.mediaType === 'image' && (
              <img
                src={currentQ.mediaUrl}
                alt="Question media"
                className={styles.mediaImage}
              />
            )}
            {currentQ.mediaType === 'video' && (
              <video
                src={currentQ.mediaUrl}
                controls
                className={styles.mediaVideo}
              />
            )}
            {currentQ.mediaType === 'audio' && (
              <div className={styles.mediaAudio}>
                <audio src={currentQ.mediaUrl} controls />
              </div>
            )}
          </div>
        )}

        <h2 className={styles.questionTitle}>{currentQ.question}</h2>

        <div className={styles.questionType}>
          {currentQ.questionType === 'single'
            ? 'Выберите один правильный ответ'
            : `Выберите все правильные ответы (${currentQ.points} баллов, частично правильный ответ дает меньше баллов)`}
        </div>

        <AnswerList
          options={currentQ.options}
          selectedAnswers={selectedAnswers}
          correctAnswers={currentQ.correctAnswers}
          questionType={currentQ.questionType}
          isAnswered={isAnswered}
          onSelect={toggleAnswer}
        />

        {isAnswered && (
          <div
            className={`${styles.resultMessage} ${
              calculatePartialScore() === currentQ.points
                ? styles.resultMessageCorrect
                : calculatePartialScore() > 0
                  ? styles.resultMessagePartial
                  : styles.resultMessageIncorrect
            }`}
          >
            {calculatePartialScore() === currentQ.points ? (
              <p>✓ Правильно! +{currentQ.points} баллов</p>
            ) : calculatePartialScore() > 0 ? (
              <p>
                ~ Частично правильно! +{calculatePartialScore()} баллов из{' '}
                {currentQ.points}
              </p>
            ) : (
              <p>✗ Неправильно! +0 баллов</p>
            )}
          </div>
        )}
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
