import { useState } from 'react'

import { useAdminQuizzes } from '@entities/quiz'
import { QuizSearch, useAdminSearch } from '@features'
import { RejectQuizDialog, ViewQuizDialog } from '@shared'
import { AdminPanelHeader, QuizTabs, StatsCards } from '@widgets'
import { toast } from 'sonner'

import styles from './AdminPanel.module.scss'

export function AdminPanel({ onBack }) {
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedQuiz, setSelectedQuiz] = useState(null)
  const [isRejectDialogOpen, setIsRejectDialogOpen] = useState(false)
  const [isViewDialogOpen, setIsViewDialogOpen] = useState(false)
  const [filterStatus, setFilterStatus] = useState('pending')
  const [currentPage, setCurrentPage] = useState(1)

  const {
    allQuizzes,
    pending,
    approved,
    rejected,
    loading,
    error,
    handleApprove: doApprove,
    handleReject: doReject,
    fetchAll,
  } = useAdminQuizzes()

  const searchedQuizzes = useAdminSearch(allQuizzes, searchQuery)

  const handleFilterChange = (newStatus) => {
    setFilterStatus(newStatus)
    setCurrentPage(1)
  }

  const handleApprove = async (quiz) => {
    try {
      await doApprove(quiz)
      toast.success('Квиз одобрен и опубликован')
    } catch {
      toast.error('Не удалось одобрить квиз')
    }
  }

  const handleRejectClick = (quiz) => {
    setSelectedQuiz(quiz)
    setIsRejectDialogOpen(true)
  }

  const handleViewClick = (quiz) => {
    setSelectedQuiz(quiz)
    setIsViewDialogOpen(true)
  }

  const handleRejectConfirm = async () => {
    if (!selectedQuiz) return
    try {
      await doReject(selectedQuiz)
      toast.success('Квиз отклонён')
    } catch {
      toast.error('Не удалось отклонить квиз')
    }
    setIsRejectDialogOpen(false)
    setSelectedQuiz(null)
  }

  const handleDeleteQuiz = async () => {
    await fetchAll()
  }

  if (loading) return <div style={{ padding: 32 }}>Загрузка...</div>
  if (error) return <div style={{ padding: 32, color: 'red' }}>{error}</div>

  return (
    <div className={styles.adminPanel}>
      <div className={styles.container}>
        <AdminPanelHeader onBack={onBack} />

        <StatsCards
          pendingCount={pending.length}
          approvedCount={approved.length}
          rejectedCount={rejected.length}
        />

        <QuizSearch query={searchQuery} onQueryChange={setSearchQuery} />

        <QuizTabs
          quizzes={searchedQuizzes}
          filterStatus={filterStatus}
          onFilterChange={handleFilterChange}
          currentPage={currentPage}
          onPageChange={setCurrentPage}
          onApprove={handleApprove}
          onReject={handleRejectClick}
          onView={handleViewClick}
          onDelete={handleDeleteQuiz}
        />
      </div>

      <ViewQuizDialog
        isOpen={isViewDialogOpen}
        quiz={selectedQuiz}
        onClose={() => setIsViewDialogOpen(false)}
        onApprove={handleApprove}
        onRejectClick={handleRejectClick}
        onDelete={handleDeleteQuiz}
      />

      <RejectQuizDialog
        isOpen={isRejectDialogOpen}
        quiz={selectedQuiz}
        onClose={() => setIsRejectDialogOpen(false)}
        onConfirm={handleRejectConfirm}
      />
    </div>
  )
}
