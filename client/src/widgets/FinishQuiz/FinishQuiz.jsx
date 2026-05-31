import React from 'react'

import { getGrade, getMessage, getMotivation } from '@features'
import { ROUTES } from '@shared'
import { Trophy, Award, Target, Clock, Home, RotateCcw } from 'lucide-react'
import { useLocation, Link } from 'react-router-dom'

import styles from './FinishQuiz.module.scss'

export function FinishQuiz() {
  const { state } = useLocation()

  const {
    quizTitle,
    maxPossibleScore,
    percentScore,
    correctCount,
    totalQuestions,
  } = state
  const grade = getGrade(percentScore)
  return (
    <div className={styles.container}>
      <section className={styles.result}>
        <div className={styles.score}>
          <div className={styles.trophyWrapper}>
            <Trophy />
          </div>
          <div className={styles.message}>{getMessage(percentScore)}</div>
          <div className={styles.quizTitle}>Квиз "{quizTitle}" завершен</div>

          <div className={styles.percentage}>
            {percentScore} из {maxPossibleScore} баллов
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
          <Link to={ROUTES.quiz} className={styles.buttonRetry}>
            <RotateCcw />
            <span>Пройти еще раз</span>
          </Link>
        </div>
      </section>

      <section className={styles.motivation}>
        {getMotivation(percentScore)}
      </section>
    </div>
  )
}
