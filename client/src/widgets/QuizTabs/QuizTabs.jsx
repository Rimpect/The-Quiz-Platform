import { myQuizzes } from '../../MockData/myQuizzes'
import { Pagination } from '../Pagination/Pagination'
import { QuizInfo } from '../QuizInfo/QuizInfo'

import styles from './QuizTabs.module.scss'

export function QuizTabs({
  quizzes: externalQuizzes,
  filterStatus,
  onFilterChange,
  currentPage,
  onPageChange,
  onApprove,
  onReject,
  onView,
}) {
  const allQuizzes =
    externalQuizzes && externalQuizzes.length > 0 ? externalQuizzes : myQuizzes

  const filteredQuizzes =
    filterStatus === 'all'
      ? allQuizzes
      : allQuizzes.filter((quiz) => quiz.status === filterStatus)

  const ITEMS_PER_PAGE = 8
  const totalPages = Math.ceil(filteredQuizzes.length / ITEMS_PER_PAGE)
  const startIndex = (currentPage - 1) * ITEMS_PER_PAGE
  const paginatedQuizzes = filteredQuizzes.slice(
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
    pending: allQuizzes.filter((q) => q.status === 'pending').length,
    approved: allQuizzes.filter((q) => q.status === 'approved').length,
    rejected: allQuizzes.filter((q) => q.status === 'rejected').length,
    all: allQuizzes.length,
  }

  const handleFilterChange = (status) => {
    onFilterChange(status)
  }

  return (
    <div className={styles.contentCard}>
      <div className={styles.tabsList}>
        {tabs.map((tab) => (
          <button
            key={tab.id}
            className={`${styles.tabTrigger} ${filterStatus === tab.id ? styles.active : ''}`}
            onClick={() => handleFilterChange(tab.id)}
          >
            {tab.label} ({counts[tab.id]})
          </button>
        ))}
      </div>

      <div className={styles.tabContent}>
        {filteredQuizzes.length === 0 ? (
          <div className={styles.emptyState}>
            <span className={styles.emptyIcon}>👥</span>
            <p>Квизы не найдены</p>
          </div>
        ) : (
          <>
            <div className={styles.paginationInfo}>
              Показано {startIndex + 1}-
              {Math.min(startIndex + ITEMS_PER_PAGE, filteredQuizzes.length)} из{' '}
              {filteredQuizzes.length}
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
