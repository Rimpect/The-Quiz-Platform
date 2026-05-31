import styles from './AnswerList.module.scss'
import { AnswerOption } from './AnswerOption'

export function AnswerList({
  options,
  questionType,
  selectedAnswers,
  correctAnswers,
  isAnswered,
  onSelect,
}) {
  return (
    <div className={styles.answersContainer}>
      {options.map((option, index) => (
        <AnswerOption
          key={index}
          index={index}
          text={option}
          questionType={questionType}
          selectedAnswers={selectedAnswers}
          correctAnswers={correctAnswers}
          isAnswered={isAnswered}
          onSelect={onSelect}
        />
      ))}
    </div>
  )
}
