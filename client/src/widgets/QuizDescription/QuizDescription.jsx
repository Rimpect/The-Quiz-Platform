import React from 'react'

import { useLeaderboard } from '@entities/leaderboard'
import {
  Badge,
  Button,
  ROUTES,
  getQuizRoute,
  getLeaderboardRatingRoute,
  getDifficulty,
  QUIZ_MODE_LABELS,
} from '@shared'
import { ArrowLeft, Users, Clock, Trophy, Award } from 'lucide-react'
import { useParams, Link } from 'react-router-dom'

import styles from './QuizDescription.module.scss'

const DEFAULT_COVER = '/placeholder-quiz.png'

const pluralRu = (n, forms) => {
  const m10 = n % 10
  const m100 = n % 100
  if (m10 === 1 && m100 !== 11) return forms[0]
  if (m10 >= 2 && m10 <= 4 && (m100 < 10 || m100 >= 20)) return forms[1]
  return forms[2]
}

export function QuizDescription({ quiz }) {
  const { id } = useParams()
  const quizMode = quiz?.quiz_mode
  const isCompetitive = quizMode === 'competitive'
  const showModeBadge = quizMode && quizMode !== 'single' && quizMode !== 'solo'

  const { leaderboard } = useLeaderboard(id)
  const bestScore = leaderboard?.[0]?.percent ?? null

  const quizData = {
    title: quiz?.title || 'Квиз',
    description: quiz?.description || '',
    category: quiz?.category || '',
    difficulty: quiz?.difficulty,
    participants: quiz?.participants ?? 0,
    duration: quiz?.duration || 0,
    questionCount: quiz?.questionCount ?? 0,
    author: quiz?.author || '',
    image: quiz?.img || quiz?.image || DEFAULT_COVER,
  }

  const difficulty = getDifficulty(quizData.difficulty)

  return (
    <div className={styles.description}>
      <div className={styles.container}>
        {/* Навигация */}
        <Link to={ROUTES.main} className={styles.nav}>
          <ArrowLeft className={styles.navIcon} />
          <span>Назад к списку</span>
        </Link>

        {/* Основной контент */}
        <div className={styles.content}>
          {/* Картинка с оверлеем */}
          <div className={styles.picture}>
            <img
              src={quizData.image}
              alt={quizData.title}
              className={styles.img}
              onError={(e) => {
                e.currentTarget.src = DEFAULT_COVER
              }}
            />
            <div className={styles.overlay}>
              <div className={styles.overlayContent}>
                <div className={styles.meta}>
                  <Trophy className={styles.metaIcon} />
                  {quizData.category && (
                    <span className={styles.metaCategory}>
                      {quizData.category}
                    </span>
                  )}
                  <Badge variant={difficulty.variant} size="sm">
                    {difficulty.label}
                  </Badge>
                  {showModeBadge && (
                    <Badge variant={quizMode} size="sm">
                      {QUIZ_MODE_LABELS[quizMode] || quizMode}
                    </Badge>
                  )}
                </div>
                <h1 className={styles.title}>{quizData.title}</h1>
              </div>
            </div>
          </div>

          {/* Две колонки */}
          <div className={styles.columns}>
            {/* Левая колонка - описание */}
            <div>
              <h2 className={styles.infoTitle}>О квизе</h2>
              {quizData.description && (
                <p className={styles.infoText}>{quizData.description}</p>
              )}

              <div className={styles.card}>
                <h3 className={styles.cardTitle}>Что вас ждет?</h3>
                <ul className={styles.cardList}>
                  <li className={styles.cardItem}>
                    • {quizData.questionCount}{' '}
                    {pluralRu(quizData.questionCount, [
                      'интересный вопрос',
                      'интересных вопроса',
                      'интересных вопросов',
                    ])}
                  </li>
                  <li className={styles.cardItem}>
                    • Ограничение по времени на каждый вопрос
                  </li>
                  <li className={styles.cardItem}>
                    • Мгновенная проверка ответов
                  </li>
                </ul>
              </div>
            </div>

            {/* Правая колонка - статистика и кнопка */}
            <div>
              <h2 className={styles.statsTitle}>Статистика</h2>

              <ul className={styles.statsList}>
                <li className={styles.statsItem}>
                  <div className={styles.statsLeft}>
                    <span className={styles.statsIcon}>
                      <Users />
                    </span>
                    <span className={styles.statsLabel}>Участников:</span>
                  </div>
                  <span className={styles.statsValue}>
                    {quizData.participants.toLocaleString()}
                  </span>
                </li>

                <li className={styles.statsItem}>
                  <div className={styles.statsLeft}>
                    <span className={styles.statsIcon}>
                      <Clock />
                    </span>
                    <span className={styles.statsLabel}>Длительность:</span>
                  </div>
                  <span className={styles.statsValue}>
                    {quizData.duration
                      ? `${quizData.duration} ${pluralRu(quizData.duration, [
                          'минута',
                          'минуты',
                          'минут',
                        ])}`
                      : 'без лимита'}
                  </span>
                </li>

                <li className={styles.statsItem}>
                  <div className={styles.statsLeft}>
                    <span className={styles.statsIcon}>
                      <Award />
                    </span>
                    <span className={styles.statsLabel}>Лучший результат:</span>
                  </div>
                  <span className={styles.statsValue}>
                    {bestScore != null ? `${bestScore}%` : '—'}
                  </span>
                </li>

                <li className={styles.statsItem}>
                  <div className={styles.statsLeft}>
                    <span className={styles.statsIcon}>
                      <Trophy />
                    </span>
                    <span className={styles.statsLabel}>Вопросов:</span>
                  </div>
                  <span className={styles.statsValue}>
                    {quizData.questionCount}
                  </span>
                </li>
                {quizData.author && (
                  <li className={styles.statsItem}>
                    <div className={styles.statsLeft}>
                      <span className={styles.statsIcon}>
                        <Award />
                      </span>
                      <span className={styles.statsLabel}>Автор:</span>
                    </div>
                    <span className={styles.statsValue}>{quizData.author}</span>
                  </li>
                )}
              </ul>
              <Link to={getQuizRoute(id)}>
                <Button variant="black" size="medium" fullWidth>
                  Начать квиз
                </Button>
              </Link>

              {isCompetitive && (
                <Link
                  to={getLeaderboardRatingRoute(id)}
                  state={{ quizMode: 'competitive' }}
                  className={styles.leaderboardLink}
                >
                  <Button variant="white" size="medium" fullWidth>
                    <Trophy size={18} />
                    Таблица лидеров
                  </Button>
                </Link>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
