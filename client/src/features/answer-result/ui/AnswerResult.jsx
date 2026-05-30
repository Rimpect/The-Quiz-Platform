export function AnswerResult({ isAnswered, score, maxScore, points }) {
  if (!isAnswered) return null

  const isFull = score === points
  const isPartial = score > 0 && score < points

  return (
    <div>
      {isFull && <p>✓ Правильно! +{points} баллов</p>}

      {isPartial && (
        <p>
          ~ Частично правильно! +{score} баллов из {points}
        </p>
      )}

      {score === 0 && <p>✗ Неправильно! +0 баллов</p>}
    </div>
  )
}
