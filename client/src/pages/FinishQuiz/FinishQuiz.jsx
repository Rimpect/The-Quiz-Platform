import React from 'react'

import { Trophy, Award, Target, Clock, Home, RotateCcw } from 'lucide-react'

import styles from './FinishQuiz.module.scss'

export default function FinishQuiz() {
  return (
    <div className={styles.container}>
      <section className={styles.result}>
        <div className={styles.score}>
          <div className={styles.trophyWrapper}>
            <Trophy />
          </div>
          <div className={styles.message}>
            Хорошая работа!👏 (разные фразы в зависимости от оценки)
          </div>
          <div className={styles.quizTitle}>
            Квиз "Научные открытия" завершен
          </div>
          <div className={styles.gradeLabel}>Оценка</div>
          <div className={styles.gradeValue}>A</div>
          <div className={styles.percentage}>85%</div>
        </div>

        <div className={styles.stats}>
          <div className={`${styles.statCard} ${styles.correct}`}>
            <Target />
            <div className={styles.statValue}>10</div>
            <div className={styles.statLabel}>Правильно</div>
          </div>
          <div className={`${styles.statCard} ${styles.wrong}`}>
            <Award />
            <div className={styles.statValue}>0</div>
            <div className={styles.statLabel}>Ошибок</div>
          </div>
          <div className={`${styles.statCard} ${styles.total}`}>
            <Clock />
            <div className={styles.statValue}>10</div>
            <div className={styles.statLabel}>Всего вопросов</div>
          </div>
        </div>

        <div className={styles.buttons}>
          <div className={styles.buttonHome}>
            <Home />
            На главную
          </div>
          <div className={styles.buttonRetry}>
            <RotateCcw />
            Пройти еще раз
          </div>
        </div>
      </section>

      <section className={styles.motivation}>
        Каждая попытка делает вас умнее! Попробуйте пройти квиз снова или
        выберите другой.
      </section>
    </div>
  )
}
