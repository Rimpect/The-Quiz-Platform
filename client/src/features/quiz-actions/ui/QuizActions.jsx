export function QuizActions({
  isAnswered,
  selectedAnswers,
  isLastQuestion,
  onSubmit,
  onNext,
}) {
  return (
    <div>
      {!isAnswered ? (
        <button onClick={onSubmit} disabled={selectedAnswers.length === 0}>
          Ответить
        </button>
      ) : (
        <button onClick={onNext}>
          {isLastQuestion ? 'Завершить квиз' : 'Следующий вопрос'}
        </button>
      )}

      <button onClick={onNext}>Пропустить вопрос</button>
    </div>
  )
}
