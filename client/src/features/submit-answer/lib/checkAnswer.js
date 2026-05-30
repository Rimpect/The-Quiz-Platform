export function checkAnswer(selectedAnswers, correctAnswers) {
  return (
    selectedAnswers.length === correctAnswers.length &&
    selectedAnswers.every((ans, i) => ans === correctAnswers[i])
  )
}
