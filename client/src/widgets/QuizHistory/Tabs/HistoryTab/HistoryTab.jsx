import { Pagination } from '@shared'

import styles from './HistoryTab.module.scss'

export function HistoryTab({
  recentQuizzes = [],
  currentPage,
  totalPages,
  onPageChange,
}) {
  const getScoreColor = (score) => {
    if (score >= 90) return styles.scoreHigh
    if (score >= 70) return styles.scoreMedium
    if (score >= 50) return styles.scoreLow
    return styles.scoreVeryLow
  }

  return (
    <div className={styles.tabContent}>
      <div className={styles.tabHeader}>
        <h2 className={styles.tabTitle}>
          История квизов ({recentQuizzes.length})
        </h2>
      </div>
      <div className={styles.quizzesList}>
        {recentQuizzes.map((quiz) => (
          <div key={quiz.id} className={styles.quizItem}>
            <div className={styles.quizContent}>
              <div className={styles.quizInfo}>
                <h3 className={styles.quizTitle}>{quiz.title}</h3>
                <p className={styles.quizCategory}>{quiz.category}</p>
                <div className={styles.quizMeta}>
                  <span>
                    {quiz.correctAnswers}/{quiz.totalQuestions} правильных
                  </span>
                  <span>•</span>
                  <span>{quiz.time}</span>
                  <span>•</span>
                  <span>{quiz.date}</span>
                </div>
              </div>
              <div
                className={`${styles.quizScore} ${getScoreColor(quiz.score)}`}
              >
                {quiz.score}%
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className={styles.paginationWrapper}>
        <Pagination
          variant="main"
          pageInfo="hidden"
          currentPage={currentPage}
          totalPages={totalPages}
          onPageChange={onPageChange}
        />
      </div>
    </div>
  )
}
