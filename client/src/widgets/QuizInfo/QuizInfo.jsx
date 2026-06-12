import { useState } from 'react'

import { Badge, Button, client, ConfirmDialog } from '@shared'
import { Eye, Dot, Users, Check, X, Trash2 } from 'lucide-react'
import { toast } from 'sonner'

import styles from './QuizInfo.module.scss'

export function QuizInfo({ quiz, onApprove, onReject, onView, onDelete }) {
  const [confirmOpen, setConfirmOpen] = useState(false)
  const [deleting, setDeleting] = useState(false)

  const handleDelete = async () => {
    setDeleting(true)
    try {
      await client(`/admin/quizzes/${quiz.id}`, { method: 'DELETE' })
      toast.success('Квиз удалён')
      setConfirmOpen(false)
      onDelete?.(quiz.id)
    } catch (e) {
      toast.error(e.message || 'Не удалось удалить квиз')
    } finally {
      setDeleting(false)
    }
  }

  const difficultyMap = {
    easy: 'easy',
    medium: 'medium',
    hard: 'hard',
    Легкий: 'easy',
    Средний: 'medium',
    Сложный: 'hard',
  }

  const difficultyLabels = {
    easy: 'Лёгкий',
    medium: 'Средний',
    hard: 'Сложный',
  }

  const statusLabels = {
    approved: 'Одобрен',
    pending: 'На модерации',
    rejected: 'Отклонен',
  }

  return (
    <div className={styles.quizCard}>
      <div className={styles.quizContent}>
        <div className={styles.quizInfo}>
          <div className={styles.quizHeader}>
            <h3 className={styles.quizTitle}>{quiz.title}</h3>
            <Badge variant={quiz.status} size="sm">
              {statusLabels[quiz.status] || quiz.status}
            </Badge>
          </div>
          <p className={styles.quizDescription}>{quiz.description}</p>
          <div className={styles.quizMeta}>
            <span className={styles.metaItem}>
              <Users /> Автор: {quiz.author}
            </span>
            <Dot />
            <span className={styles.metaItem}>Категория: {quiz.category}</span>
            <Dot />
            <span className={styles.metaItem}>
              Вопросов: {quiz.total_questions ?? quiz.questionCount ?? 0}
            </span>
            <Dot />
            <span className={styles.metaItem}>
              Сложность:
              <Badge
                variant={difficultyMap[quiz.difficulty] || 'easy'}
                size="sm"
              >
                {difficultyLabels[quiz.difficulty] ||
                  quiz.difficulty ||
                  'Лёгкий'}
              </Badge>
            </span>
            <Dot />
            <span className={styles.metaItem}>
              {quiz.created_at
                ? new Date(quiz.created_at).toLocaleDateString('ru-RU')
                : quiz.createdAt || ''}
            </span>
          </div>
        </div>

        <div className={styles.quizActions}>
          {quiz.status === 'pending' && (
            <>
              <Button
                variant="green"
                size="medium"
                icon={<Check size={20} />}
                onClick={() => onApprove(quiz)}
              >
                Одобрить
              </Button>
              <Button
                variant="red"
                size="medium"
                icon={<X size={20} />}
                onClick={() => onReject(quiz)}
              >
                Отклонить
              </Button>
            </>
          )}
          <Button
            variant="white"
            size="medium"
            icon={<Eye size={20} />}
            onClick={() => onView(quiz)}
          >
            Просмотр
          </Button>
          <Button
            variant="red"
            size="medium"
            icon={<Trash2 size={20} />}
            onClick={() => setConfirmOpen(true)}
          >
            Удалить
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
