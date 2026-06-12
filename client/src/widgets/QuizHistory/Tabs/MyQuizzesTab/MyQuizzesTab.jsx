import { Badge, Button, Pagination, ROUTES } from '@shared'
import { FileText, Plus, Edit, Trash2 } from 'lucide-react'
import { Link, useNavigate } from 'react-router-dom'
import { toast } from 'sonner'

import styles from './MyQuizzesTab.module.scss'

export function MyQuizzesTab({
  onCreateQuiz,
  myQuizzes = [],
  currentPage,
  totalPages,
  onPageChange,
  onDelete,
}) {
  const navigate = useNavigate()

  const statusLabels = {
    approved: 'Опубликован',
    pending: 'На модерации',
    rejected: 'Отклонён',
  }

  const handleEdit = (quiz) => {
    navigate(ROUTES.createQuiz, { state: { editQuizId: quiz.id } })
  }

  const handleDelete = async (quiz) => {
    if (!window.confirm(`Удалить квиз "${quiz.title}"?`)) return
    try {
      await onDelete(quiz.id)
      toast.success('Квиз удалён')
    } catch {
      toast.error('Не удалось удалить квиз')
    }
  }

  return (
    <div className={styles.tabContent}>
      <div className={styles.tabHeader}>
        <h2 className={styles.tabTitle}>
          Созданные квизы ({myQuizzes.length})
        </h2>
        <Link to={ROUTES.createQuiz}>
          <Button onClick={onCreateQuiz} icon={<Plus size={16} />}>
            Создать квиз
          </Button>
        </Link>
      </div>

      {myQuizzes.length === 0 ? (
        <div className={styles.emptyState}>
          <FileText className={styles.emptyIcon} />
          <p className={styles.emptyText}>У вас пока нет созданных квизов</p>
          <Link to={ROUTES.createQuiz}>
            <Button onClick={onCreateQuiz} icon={<Plus size={16} />}>
              Создать первый квиз
            </Button>
          </Link>
        </div>
      ) : (
        <>
          <div className={styles.quizzesList}>
            {myQuizzes.map((quiz) => (
              <div key={quiz.id} className={styles.quizItem}>
                <div className={styles.quizContent}>
                  <div className={styles.quizInfo}>
                    <div className={styles.quizHeader}>
                      <h3 className={styles.quizTitle}>{quiz.title}</h3>
                      <Badge variant={quiz.status} size="sm">
                        {statusLabels[quiz.status] || quiz.status}
                      </Badge>
                    </div>
                    <p className={styles.quizCategory}>
                      {quiz.category || 'Без категории'}
                    </p>
                    <div className={styles.quizMeta}>
                      <span>Вопросов: {quiz.total_questions || 0}</span>
                      <span>•</span>
                      <span>Участников: {quiz.participants || 0}</span>
                      <span>•</span>
                      <span>{quiz.createdAt}</span>
                    </div>
                  </div>
                  <div className={styles.quizActions}>
                    <Button
                      icon={<Edit size={16} />}
                      variant="transparent"
                      title="Редактировать"
                      onClick={() => handleEdit(quiz)}
                    />
                    <Button
                      icon={<Trash2 size={16} />}
                      variant="transparent"
                      title="Удалить"
                      onClick={() => handleDelete(quiz)}
                    />
                  </div>
                </div>
                {quiz.status === 'rejected' && (
                  <div className={styles.rejectionMessage}>
                    Квиз отклонён администратором
                  </div>
                )}
              </div>
            ))}
          </div>

          <div className={styles.paginationWrapper}>
            <Pagination
              variant="main"
              pageInfo="hidden"
              currentPage={currentPage}
              totalPages={totalPages}
              onPageChange={onPageChange}
            />
          </div>
        </>
      )}
    </div>
  )
}
