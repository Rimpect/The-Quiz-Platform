import { Button } from '@shared'

import styles from './QuizActions.module.scss'

export function QuizActions({
  isAnswered,
  selectedAnswers,
  isLastQuestion,
  onSubmit,
  onNext,
}) {
  return (
    <div className={styles.container}>
      {!isAnswered ? (
        <Button
          variant="green"
          fullWidth
          onClick={onSubmit}
          disabled={selectedAnswers.length === 0}
        >
          Ответить
        </Button>
      ) : (
        <Button variant="green" fullWidth onClick={onNext}>
          {isLastQuestion ? 'Завершить квиз' : 'Следующий вопрос'}
        </Button>
      )}

      <Button variant="red" fullWidth onClick={onNext}>
        Пропустить вопрос
      </Button>
    </div>
  )
}
