import { Badge, Button, Pagination, ROUTES } from '@shared'
import { FileText, Plus, Edit, Trash2 } from 'lucide-react'
import { Link } from 'react-router-dom'

import styles from './MyQuizzesTab.module.scss'

export function MyQuizzesTab({
  onCreateQuiz,
  myQuizzes = [],
  currentPage,
  totalPages,
  onPageChange,
}) {
  const statusLabels = {
    approved: 'Одобрен',
    pending: 'На модерации',
    rejected: 'Отклонен',
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
          <Button onClick={onCreateQuiz} icon={<Plus size={16} />}>
            Создать первый квиз
          </Button>
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
                    <p className={styles.quizCategory}>{quiz.category}</p>
                    <div className={styles.quizMeta}>
                      <span>Участников: {quiz.participants}</span>
                      {quiz.status === 'approved' && (
                        <>
                          <span>•</span>
                          <span>Рейтинг: {quiz.rating}</span>
                        </>
                      )}
                      <span>•</span>
                      <span>{quiz.createdAt}</span>
                    </div>
                  </div>
                  <div className={styles.quizActions}>
                    <Button icon={<Edit size={16} />} variant="transparent" />
                    <Button icon={<Trash2 size={16} />} variant="transparent" />
                  </div>
                </div>
                {quiz.status === 'rejected' && (
                  <div className={styles.rejectionMessage}>
                    Причина отклонения: Недостаточно уникальных вопросов
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
