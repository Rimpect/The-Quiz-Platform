import styles from './QuestionSection.module.scss'

export function QuestionSection({ question }) {
  return (
    <div className={styles.mediaContainer}>
      {question.mediaUrl && (
        <div>
          {question.mediaType === 'image' && (
            <img
              src={question.mediaUrl}
              alt="media"
              className={styles.mediaImage}
            />
          )}

          {question.mediaType === 'video' && (
            <video
              src={question.mediaUrl}
              controls
              className={styles.mediaVideo}
            />
          )}

          {question.mediaType === 'audio' && (
            <audio
              src={question.mediaUrl}
              controls
              className={styles.mediaAudio}
            />
          )}
        </div>
      )}

      <h2 className={styles.questionTitle}>{question.question}</h2>
      {/* <div
        className={`${styles.questionType} ${
          question.questionType === 'single' ? styles.single : styles.multiple
        }`}
      >
        {question.questionType === 'single'
          ? 'Один ответ'
          : 'Множественный выбор'}
      </div> */}
    </div>
  )
}
