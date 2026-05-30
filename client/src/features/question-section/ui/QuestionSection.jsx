export function QuestionSection({ question }) {
  return (
    <div>
      {question.mediaUrl && (
        <div>
          {question.mediaType === 'image' && (
            <img src={question.mediaUrl} alt="media" />
          )}

          {question.mediaType === 'video' && (
            <video src={question.mediaUrl} controls />
          )}

          {question.mediaType === 'audio' && (
            <audio src={question.mediaUrl} controls />
          )}
        </div>
      )}

      <h2>{question.question}</h2>

      <div>
        {question.questionType === 'single'
          ? 'Выберите один правильный ответ'
          : 'Выберите несколько правильных ответов'}
      </div>
    </div>
  )
}
