import { useEffect, useState } from 'react'

import { Badge, Button, client } from '@shared'
import { Eye, Check, X, Trash2 } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { toast } from 'sonner'

import { ConfirmDialog } from '../ConfirmDialog/ConfirmDialog'

import styles from './ViewQuizDialog.module.scss'

export function ViewQuizDialog({
  isOpen,
  quiz,
  onClose,
  onApprove,
  onRejectClick,
  onDelete,
}) {
  const navigate = useNavigate()
  const [fullQuiz, setFullQuiz] = useState(null)
  const [loading, setLoading] = useState(false)
  const [confirmOpen, setConfirmOpen] = useState(false)
  const [deleting, setDeleting] = useState(false)

  useEffect(() => {
    if (isOpen && quiz?.id) {
      setLoading(true)
      client(`/quizzes/${quiz.id}/full`)
        .then((data) => setFullQuiz(data))
        .catch(() => setFullQuiz(null))
        .finally(() => setLoading(false))
    }
  }, [isOpen, quiz?.id])

  if (!isOpen || !quiz) return null

  const statusLabels = {
    approved: 'Одобрен',
    pending: 'На модерации',
    rejected: 'Отклонен',
  }

  const difficultyLabels = {
    easy: 'Лёгкий',
    medium: 'Средний',
    hard: 'Сложный',
  }

  const handleDelete = async () => {
    setDeleting(true)
    try {
      await client(`/admin/quizzes/${quiz.id}`, { method: 'DELETE' })
      toast.success('Квиз удалён')
      setConfirmOpen(false)
      onClose()
      if (onDelete) onDelete(quiz.id)
    } catch (e) {
      toast.error(e.message || 'Не удалось удалить квиз')
    } finally {
      setDeleting(false)
    }
  }

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
            {/* Заголовок */}
            <div className={styles.viewQuizHeader}>
              <div>
                <h3 className={styles.viewQuizTitle}>{quiz.title}</h3>
                <Badge variant={quiz.status} size="sm">
                  {statusLabels[quiz.status] || quiz.status}
                </Badge>
              </div>
            </div>

            {/* Основные детали */}
            <div className={styles.viewQuizDetails}>
              <div className={styles.detailsGrid}>
                <div>
                  <p className={styles.detailLabel}>Автор</p>
                  <p className={styles.detailValue}>{quiz.author}</p>
                </div>
                <div>
                  <p className={styles.detailLabel}>Категория</p>
                  <p className={styles.detailValue}>{quiz.category || 'Нет'}</p>
                </div>
                <div>
                  <p className={styles.detailLabel}>Сложность</p>
                  <p className={styles.detailValue}>
                    {difficultyLabels[quiz.difficulty] || quiz.difficulty}
                  </p>
                </div>
                <div>
                  <p className={styles.detailLabel}>Вопросов</p>
                  <p className={styles.detailValue}>
                    {quiz.total_questions || 0}
                  </p>
                </div>
                <div>
                  <p className={styles.detailLabel}>Длительность</p>
                  <p className={styles.detailValue}>
                    {quiz.duration_minutes
                      ? `${quiz.duration_minutes} мин`
                      : 'без лимита'}
                  </p>
                </div>
                <div>
                  <p className={styles.detailLabel}>Тип</p>
                  <p className={styles.detailValue}>
                    {quiz.quiz_mode || 'одиночный'}
                  </p>
                </div>
              </div>

              <div className={styles.descriptionBlock}>
                <p className={styles.detailLabel}>Описание</p>
                <p className={styles.descriptionText}>{quiz.description}</p>
              </div>
            </div>

            {/* Вопросы и ответы */}
            {fullQuiz?.questions && fullQuiz.questions.length > 0 && (
              <div className={styles.questionsSection}>
                <h4 className={styles.questionsTitle}>
                  Вопросы и ответы (30 сек на проверку)
                </h4>
                {fullQuiz.questions.map((question, qIdx) => (
                  <div key={question.id} className={styles.questionBlock}>
                    <div className={styles.questionHeader}>
                      <span className={styles.questionNum}>
                        Вопрос {qIdx + 1}
                      </span>
                      <span className={styles.timeLimit}>30 сек</span>
                    </div>
                    <p className={styles.questionText}>
                      {question.question_text}
                    </p>
                    <div className={styles.answersList}>
                      {question.answers &&
                        question.answers.map((answer, aIdx) => (
                          <div
                            key={answer.id}
                            className={`${styles.answerItem} ${
                              answer.is_correct ? styles.answerCorrect : ''
                            }`}
                          >
                            <span className={styles.answerNum}>
                              {aIdx + 1}.
                            </span>
                            <span className={styles.answerText}>
                              {answer.answer_text}
                            </span>
                            {answer.is_correct && (
                              <span className={styles.checkMark}>✓</span>
                            )}
                          </div>
                        ))}
                    </div>
                  </div>
                ))}
              </div>
            )}

            {/* Действия */}
            <div className={styles.viewActions}>
              {quiz.status === 'pending' && (
                <>
                  <Button
                    variant="green"
                    fullWidth
                    icon={<Check size={18} />}
                    onClick={() => onApprove(quiz)}
                  >
                    Одобрить
                  </Button>
                  <Button
                    variant="red"
                    fullWidth
                    icon={<X size={18} />}
                    onClick={() => onRejectClick(quiz)}
                  >
                    Отклонить
                  </Button>
                </>
              )}

              <Button
                variant="red"
                fullWidth
                icon={<Trash2 size={18} />}
                onClick={() => setConfirmOpen(true)}
              >
                Удалить
              </Button>

              <Button
                variant="transparent"
                fullWidth
                icon={<Eye size={18} />}
                onClick={() => {
                  onClose()
                  navigate(`/quiz/${quiz.id}`)
                }}
              >
                Посмотреть на сайте
              </Button>
            </div>
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
