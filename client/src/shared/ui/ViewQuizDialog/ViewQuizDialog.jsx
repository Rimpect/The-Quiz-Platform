import { Button } from '@shared'

import { ConfirmDialog } from '../ConfirmDialog/ConfirmDialog'

import styles from './ViewQuizDialog.module.scss'
import { useViewQuizDialog } from './model/useViewQuizDialog'
import { QuizDetails } from './ui/QuizDetails'
import { QuizQuestionsPreview } from './ui/QuizQuestionsPreview'
import { ViewQuizActions } from './ui/ViewQuizActions'

export function ViewQuizDialog({
  isOpen,
  quiz,
  onClose,
  onApprove,
  onRejectClick,
  onDelete,
}) {
  const { fullQuiz, loading, confirmOpen, setConfirmOpen, deleting, handleDelete } =
    useViewQuizDialog(quiz, isOpen, { onClose, onDelete })

  if (!isOpen || !quiz) return null

  return (
    <div className={styles.dialogOverlay} onClick={onClose}>
      <div
        className={styles.dialogContent}
        onClick={(e) => e.stopPropagation()}
      >
        <div className={styles.dialogHeader}>
          <h2 className={styles.dialogTitle}>Просмотр квиза</h2>
          <p className={styles.dialogDescription}>Детальная информация</p>
        </div>

        {loading ? (
          <div
            className={styles.dialogBody}
            style={{ textAlign: 'center', padding: '2rem' }}
          >
            Загрузка...
          </div>
        ) : (
          <div className={styles.dialogBody}>
            <QuizDetails quiz={quiz} />
            <QuizQuestionsPreview questions={fullQuiz?.questions} />
            <ViewQuizActions
              quiz={quiz}
              onApprove={onApprove}
              onRejectClick={onRejectClick}
              onDeleteClick={() => setConfirmOpen(true)}
              onClose={onClose}
            />
          </div>
        )}

        <div className={styles.dialogFooter}>
          <Button variant="transparent" fullWidth onClick={onClose}>
            Закрыть
          </Button>
        </div>
      </div>

      <ConfirmDialog
        isOpen={confirmOpen}
        title="Удалить квиз?"
        message={`Квиз "${quiz.title}" будет удалён безвозвратно.`}
        loading={deleting}
        onConfirm={handleDelete}
        onCancel={() => setConfirmOpen(false)}
      />
    </div>
  )
}
