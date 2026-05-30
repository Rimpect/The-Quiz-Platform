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

  return (
    <div onClick={() => onSelect(index)}>
      {questionType === 'single' ? (
        <input type="radio" checked={isSelected} readOnly />
      ) : (
        <input type="checkbox" checked={isSelected} readOnly />
      )}

      <span>{text}</span>

      {isAnswered && isCorrect && <span>✓</span>}

      {isAnswered && isSelected && !isCorrect && <span>✗</span>}
    </div>
  )
}
