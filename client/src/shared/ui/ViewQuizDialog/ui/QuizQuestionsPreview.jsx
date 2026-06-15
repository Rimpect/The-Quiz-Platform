import styles from '../ViewQuizDialog.module.scss'

export function QuizQuestionsPreview({ questions }) {
  if (!questions || questions.length === 0) return null

  return (
    <div className={styles.questionsSection}>
      <h4 className={styles.questionsTitle}>
        Вопросы и ответы (30 сек на проверку)
      </h4>
      {questions.map((question, qIdx) => (
        <div key={question.id} className={styles.questionBlock}>
          <div className={styles.questionHeader}>
            <span className={styles.questionNum}>Вопрос {qIdx + 1}</span>
            <span className={styles.timeLimit}>30 сек</span>
          </div>
          <p className={styles.questionText}>{question.question_text}</p>
          <div className={styles.answersList}>
            {question.answers &&
              question.answers.map((answer, aIdx) => (
                <div
                  key={answer.id}
                  className={`${styles.answerItem} ${
                    answer.is_correct ? styles.answerCorrect : ''
                  }`}
                >
                  <span className={styles.answerNum}>{aIdx + 1}.</span>
                  <span className={styles.answerText}>{answer.answer_text}</span>
                  {answer.is_correct && (
                    <span className={styles.checkMark}>✓</span>
                  )}
                </div>
              ))}
          </div>
        </div>
      ))}
    </div>
  )
}
