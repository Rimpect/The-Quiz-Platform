import styles from './QuizInfoCard.module.scss'

export function QuizInfoCard({ quiz }) {
  return (
    <div className={styles.card}>
      <h3>Информация о квизе</h3>

      <div className={styles.row}>
        <span>Вопросов</span>
        <span>{quiz.questionCount}</span>
      </div>

      <div className={styles.row}>
        <span>Длительность</span>
        <span>{quiz.duration} мин</span>
      </div>

      <div className={styles.row}>
        <span>Сложность</span>
        <span>{quiz.difficulty}</span>
      </div>
    </div>
  )
}
