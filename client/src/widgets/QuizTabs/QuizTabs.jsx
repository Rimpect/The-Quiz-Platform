import { Pagination } from '../Pagination/Pagination'
import { QuizInfo } from '../QuizInfo/QuizInfo'

import styles from './QuizTabs.module.scss'

export function QuizTabs({
  quizzes,
  filterStatus,
  onFilterChange,
  currentPage,
  onPageChange,
  onApprove,
  onReject,
  onView,
}) {
  const ITEMS_PER_PAGE = 8
  const totalPages = Math.ceil(quizzes.length / ITEMS_PER_PAGE)
  const startIndex = (currentPage - 1) * ITEMS_PER_PAGE
  const paginatedQuizzes = quizzes.slice(
    startIndex,
    startIndex + ITEMS_PER_PAGE,
  )

  const tabs = [
    { id: 'pending', label: 'На модерации' },
    { id: 'approved', label: 'Одобренные' },
    { id: 'rejected', label: 'Отклоненные' },
    { id: 'all', label: 'Все' },
  ]

  const counts = {
    pending: quizzes.filter((q) => q.status === 'pending').length,
    approved: quizzes.filter((q) => q.status === 'approved').length,
    rejected: quizzes.filter((q) => q.status === 'rejected').length,
    all: quizzes.length,
  }

  return (
    <div className={styles.contentCard}>
      <div className={styles.tabsList}>
        {tabs.map((tab) => (
          <button
            key={tab.id}
            className={`${styles.tabTrigger} ${filterStatus === tab.id ? styles.active : ''}`}
            onClick={() => onFilterChange(tab.id)}
          >
            {tab.label} ({counts[tab.id]})
          </button>
        ))}
      </div>

      <div className={styles.tabContent}>
        {quizzes.length === 0 ? (
          <div className={styles.emptyState}>
            <span className={styles.emptyIcon}>👥</span>
            <p>Квизы не найдены</p>
          </div>
        ) : (
          <>
            <div className={styles.paginationInfo}>
              Показано {startIndex + 1}-
              {Math.min(startIndex + ITEMS_PER_PAGE, quizzes.length)} из{' '}
              {quizzes.length}
            </div>

            {paginatedQuizzes.map((quiz) => (
              <QuizInfo
                key={quiz.id}
                quiz={quiz}
                onApprove={onApprove}
                onReject={onReject}
                onView={onView}
              />
            ))}

            <Pagination
              currentPage={currentPage}
              totalPages={totalPages}
              onPageChange={onPageChange}
            />
          </>
        )}
      </div>
    </div>
  )
}
