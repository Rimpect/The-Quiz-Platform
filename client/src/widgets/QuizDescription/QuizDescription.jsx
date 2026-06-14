import React from 'react'

import {
  Badge,
  Button,
  ROUTES,
  getQuizRoute,
  getLeaderboardRatingRoute,
} from '@shared'
import { ArrowLeft, Users, Clock, Trophy, Star, Award } from 'lucide-react'
import { useParams, Link } from 'react-router-dom'

import styles from './QuizDescription.module.scss'

// Русская плюрализация: forms = [одна, несколько, много]
const pluralRu = (n, forms) => {
  const m10 = n % 10
  const m100 = n % 100
  if (m10 === 1 && m100 !== 11) return forms[0]
  if (m10 >= 2 && m10 <= 4 && (m100 < 10 || m100 >= 20)) return forms[1]
  return forms[2]
}

export function QuizDescription({ quiz }) {
  const { id } = useParams()
  const isCompetitive = quiz?.quiz_mode === 'competitive'
  const quizData = {
    id: quiz?.id ?? 2,
    title: quiz?.title ?? 'Великие научные открытия',
    description:
      quiz?.description ??
      'Квиз о великих научных открытиях и изобретениях человечества',
    category: quiz?.category ?? 'Наука',
    difficulty: quiz?.difficulty ?? 'Средний',
    rating: quiz?.rating ?? 4.7,
    participants: quiz?.participants ?? 1234,
    duration: quiz?.duration ?? 45,
    topScore: quiz?.topScore ?? 98,
    questionCount: quiz?.questionCount ?? 20,
    author: quiz?.author ?? 'QuizStudio',
    language: quiz?.language ?? 'Русский',
    lastUpdated: quiz?.lastUpdated ?? '2026-01-01',
    image: quiz?.img || quiz?.image,
  }

  let difficultyVariant = 'medium'
  if (quizData.difficulty === 'Легкий') {
    difficultyVariant = 'easy'
  } else if (quizData.difficulty === 'Сложный') {
    difficultyVariant = 'hard'
  }

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
            />
            <div className={styles.overlay}>
              <div className={styles.overlayContent}>
                <div className={styles.meta}>
                  <Trophy className={styles.metaIcon} />
                  <span className={styles.metaCategory}>
                    {quizData.category}
                  </span>
                  <Badge variant={difficultyVariant} size="sm">
                    {quizData.difficulty}
                  </Badge>
                </div>
                <h1 className={styles.title}>{quizData.title}</h1>
                <div className={styles.rating}>
                  <Star className={styles.ratingIcon} />
                  <span className={styles.ratingValue}>{quizData.rating}</span>
                </div>
              </div>
            </div>
          </div>

          {/* Две колонки */}
          <div className={styles.columns}>
            {/* Левая колонка - описание */}
            <div>
              <h2 className={styles.infoTitle}>О квизе</h2>
              <p className={styles.infoText}>{quizData.description}</p>

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
                  <li className={styles.cardItem}>
                    • Подробная статистика в конце
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
                    {quizData.duration} минут
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
                    {quizData.topScore}%
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
                <li className={styles.statsItem}>
                  <div className={styles.statsLeft}>
                    <span className={styles.statsIcon}>
                      <Award />
                    </span>
                    <span className={styles.statsLabel}>Автор:</span>
                  </div>
                  <span className={styles.statsValue}>{quizData.author}</span>
                </li>
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
