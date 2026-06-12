import { Avatar, Input } from '@shared'

import styles from './AnswerOption.module.scss'

export function AnswerOption({
  index,
  text,
  questionType,
  selectedAnswers,
  correctAnswers,
  isAnswered,
  onSelect,
  voters,
}) {
  const isSelected = selectedAnswers.includes(index)
  const isCorrect = correctAnswers.includes(index)

  const className = `
    ${styles.answerOption}
    ${!isAnswered && isSelected ? styles.selected : ''}
    ${isAnswered && isCorrect ? styles.correct : ''}
    ${isAnswered && isSelected && !isCorrect ? styles.incorrect : ''}
    ${isAnswered && !isSelected && !isCorrect ? styles.disabled : ''}
  `

  return (
    <div className={className} onClick={() => onSelect(index)}>
      {questionType === 'multiple' && (
        <Input
          type="checkbox"
          checked={isSelected}
          readOnly
          className={styles.answerCheckbox}
        />
      )}

      <span className={styles.answerText}>{text}</span>

      {voters?.length > 0 && (
        <span className={styles.voters}>
          {voters.slice(0, 5).map((v, i) => (
            <span key={i} className={styles.voter} title={v.nickname}>
              <Avatar src={v.avatar} alt={v.nickname} size={26} />
            </span>
          ))}
          {voters.length > 5 && (
            <span className={styles.voterMore}>+{voters.length - 5}</span>
          )}
        </span>
      )}

      {isAnswered && isCorrect && (
        <span className={`${styles.resultIcon} ${styles.resultIconCorrect}`}>
          ✓
        </span>
      )}

      {isAnswered && isSelected && !isCorrect && (
        <span className={`${styles.resultIcon} ${styles.resultIconIncorrect}`}>
          ✗
        </span>
      )}
    </div>
  )
}
