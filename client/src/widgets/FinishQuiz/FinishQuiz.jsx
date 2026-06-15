import React, { useEffect, useRef, useState } from 'react'

import { ACHIEVEMENTS_LIST } from '@entities/achievement'
import { getGrade, getMessage, getMotivation } from '@features'
import { ROUTES, getQuizRoute } from '@shared'
import { client } from '@shared/api/client'
import {
  Trophy,
  Award,
  Target,
  Clock,
  Home,
  RotateCcw,
  Users,
} from 'lucide-react'
import { useLocation, Link, useParams } from 'react-router-dom'
import { toast } from 'sonner'

import styles from './FinishQuiz.module.scss'

export function FinishQuiz() {
  const { state } = useLocation()
  const { id } = useParams()
  const savedRef = useRef(false)
  const [leaderboard, setLeaderboard] = useState([])
  const [loadingLeaderboard, setLoadingLeaderboard] = useState(false)

  const {
    quizTitle,
    maxPossibleScore,
    percentScore,
    correctCount,
    totalQuestions,
    totalScore = 0,
    durationSeconds = 0,
    quizMode,
  } = state || {}

  const grade = getGrade(percentScore)

  useEffect(() => {
    if ((quizMode === 'team' || quizMode === 'competitive') && id) {
      setLoadingLeaderboard(true)
      client(`/quizzes/${id}/leaderboard`)
        .then((data) => {
          setLeaderboard(data || [])
        })
        .catch((err) => {
          console.error('Failed to load leaderboard:', err)
          setLeaderboard([])
        })
        .finally(() => setLoadingLeaderboard(false))
    }
  }, [id, quizMode])

  useEffect(() => {
    // Сохраняет один раз (защита от повторного рендера)
    if (savedRef.current || !id) return
    savedRef.current = true

    const save = async () => {
      try {
        const data = await client('/quiz-results/save', {
          method: 'POST',
          body: JSON.stringify({
            quiz_id: Number(id),
            score: totalScore,
            max_score: maxPossibleScore || 0,
            duration_seconds: durationSeconds,
          }),
        })

        const newlyUnlocked = data?.newly_unlocked || []
        newlyUnlocked.forEach((achId) => {
          const ach = ACHIEVEMENTS_LIST.find((a) => a.id === achId)
          if (ach) {
            toast.success(
              `${ach.icon} Достижение разблокировано: ${ach.title}`,
              {
                duration: 5000,
              },
            )
          }
        })
      } catch (e) {
        console.error('Failed to save quiz result:', e)
      }
    }

    save()
  }, [id])

  return (
    <div className={styles.container}>
      <section className={styles.result}>
        <div className={styles.score}>
          <div className={styles.trophyWrapper}>
            <Trophy />
          </div>
          <div className={styles.message}>{getMessage(percentScore)}</div>
          <div className={styles.quizTitle}>Квиз "{quizTitle}" завершен</div>

          <div className={styles.percentBig}>{percentScore}%</div>
          <div className={styles.percentage}>
            {totalScore} из {maxPossibleScore} баллов
          </div>
          <div className={styles.gradeRow}>
            <span className={styles.gradeLabel}>Оценка:</span>
            <span className={styles.gradeValue}>{grade}</span>
          </div>
        </div>

        <div className={styles.stats}>
          <div className={`${styles.statCard} ${styles.correct}`}>
            <Target />
            <div className={styles.statValue}>{correctCount}</div>
            <div className={styles.statLabel}>Правильно</div>
          </div>
          <div className={`${styles.statCard} ${styles.wrong}`}>
            <Award />
            <div className={styles.statValue}>
              {totalQuestions - correctCount}
            </div>
            <div className={styles.statLabel}>Ошибок</div>
          </div>
          <div className={`${styles.statCard} ${styles.total}`}>
            <Clock />
            <div className={styles.statValue}>{totalQuestions}</div>
            <div className={styles.statLabel}>Всего вопросов</div>
          </div>
        </div>

        <div className={styles.buttons}>
          <Link to={ROUTES.main} className={styles.buttonHome}>
            <Home />
            <span>На главную</span>
          </Link>
          <Link to={getQuizRoute(id)} className={styles.buttonRetry}>
            <RotateCcw />
            <span>Пройти еще раз</span>
          </Link>
        </div>
      </section>

      <section className={styles.motivation}>
        {getMotivation(percentScore)}
      </section>

      {(quizMode === 'team' || quizMode === 'competitive') && (
        <section className={styles.leaderboard}>
          <div className={styles.leaderboardHeader}>
            <Users size={24} />
            <h2>
              {quizMode === 'team' ? 'Результаты команды' : 'Таблица лидеров'}
            </h2>
          </div>

          {loadingLeaderboard ? (
            <div className={styles.loadingMessage}>Загрузка результатов...</div>
          ) : leaderboard.length === 0 ? (
            <div className={styles.emptyMessage}>Нет результатов</div>
          ) : (
            <div className={styles.leaderboardList}>
              {leaderboard.map((item, index) => (
                <div key={index} className={styles.leaderboardItem}>
                  <div className={styles.place}>
                    {index === 0
                      ? '🥇'
                      : index === 1
                        ? '🥈'
                        : index === 2
                          ? '🥉'
                          : `#${index + 1}`}
                  </div>
                  <div className={styles.playerInfo}>
                    <div className={styles.playerName}>
                      {item.name || 'Игрок'}
                    </div>
                    <div className={styles.playerStats}>
                      {item.percent}% • {item.time || '0:00'}
                    </div>
                  </div>
                  <div className={styles.playerScore}>{item.score || 0}</div>
                </div>
              ))}
            </div>
          )}
        </section>
      )}
    </div>
  )
}
