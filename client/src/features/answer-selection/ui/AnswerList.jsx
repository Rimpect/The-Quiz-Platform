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
    <div>
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
