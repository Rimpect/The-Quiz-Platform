export function calculatePartialScore(selectedAnswers, correctAnswers, points) {
  if (selectedAnswers.length === 0) return 0

  const correctSet = new Set(correctAnswers)

  let correctSelected = 0
  let incorrectSelected = 0

  selectedAnswers.forEach((answer) => {
    if (correctSet.has(answer)) {
      correctSelected++
    } else {
      incorrectSelected++
    }
  })

  const scorePerAnswer = points / correctAnswers.length

  const score =
    correctSelected * scorePerAnswer - incorrectSelected * scorePerAnswer

  return Math.max(0, Math.floor(score))
}
