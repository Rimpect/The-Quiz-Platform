import { Input } from '@shared'

import styles from './AnswerOption.module.scss'

export function AnswerOption({
  index,
  text,
  questionType,
  selectedAnswers,
  correctAnswers,
  isAnswered,
  onSelect,
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
