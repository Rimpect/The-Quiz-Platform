import styles from './AnswerResult.module.scss'

export function AnswerResult({ isAnswered, score, points }) {
  if (!isAnswered) return null

  if (score === points) {
    return (
      <div className={styles.resultMessage}>
        <p className={styles.resultMessageCorrect}>
          ✓ Правильно! +{points} баллов
        </p>
      </div>
    )
  }

  if (score > 0) {
    return (
      <div className={styles.resultMessage}>
        <p className={styles.resultMessagePartial}>
          ~ Частично правильно! +{score} баллов из {points}
        </p>
      </div>
    )
  }

  return (
    <div className={styles.resultMessage}>
      <p className={styles.resultMessageIncorrect}>✗ Неправильно! +0 баллов</p>
    </div>
  )
}
