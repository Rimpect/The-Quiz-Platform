export function QuestionCard({ question }) {
  return (
    <>
      <QuestionMedia type={question.mediaType} url={question.mediaUrl} />

      <h2>{question.question}</h2>

      <QuestionHint type={question.questionType} />
    </>
  )
}
