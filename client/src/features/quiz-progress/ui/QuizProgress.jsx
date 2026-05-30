export function QuizProgress({
  currentQuestion,
  totalQuestions,
  totalScore,
  maxPossibleScore,
}) {
  const progress = ((currentQuestion + 1) / totalQuestions) * 100

  return (
    <div>
      <div
        style={{
          width: `${progress}%`,
        }}
      />

      <div>
        <div>
          Вопрос {currentQuestion + 1} из {totalQuestions}
        </div>

        <div>
          Баллы: {totalScore} / {maxPossibleScore}
        </div>
      </div>
    </div>
  )
}
