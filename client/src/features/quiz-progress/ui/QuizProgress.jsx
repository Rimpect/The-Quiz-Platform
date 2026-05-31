import styles from './QuizProgress.module.scss'

export function QuizProgress({
  currentQuestion,
  totalQuestions,
  totalScore,
  maxPossibleScore,
}) {
  const progress = ((currentQuestion + 1) / totalQuestions) * 100

  return (
    <div className={styles.progressContainer}>
      <div className={styles.progressBar} style={{ width: `${progress}%` }} />

      <div className={styles.progressInfo}>
        <div className={styles.progressInfoText}>
          Вопрос {currentQuestion + 1} из {totalQuestions}
        </div>

        <div className={styles.progressInfoScore}>
          Баллы: {totalScore} / {maxPossibleScore}
        </div>
      </div>
    </div>
  )
}
