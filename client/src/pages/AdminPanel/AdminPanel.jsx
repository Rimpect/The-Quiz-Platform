import { useState } from 'react'

import { QuizSearch, useAdminSearch } from '@features'
import { RejectQuizDialog, ViewQuizDialog } from '@shared'
import { AdminPanelHeader, QuizTabs, StatsCards } from '@widgets'
import { toast } from 'sonner'

import { myQuizzes } from '../../MockData/myQuizzes'

import styles from './AdminPanel.module.scss'

export function AdminPanel({ onBack }) {
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedQuiz, setSelectedQuiz] = useState(null)
  const [isRejectDialogOpen, setIsRejectDialogOpen] = useState(false)
  const [isViewDialogOpen, setIsViewDialogOpen] = useState(false)
  const [filterStatus, setFilterStatus] = useState('pending')
  const [currentPage, setCurrentPage] = useState(1)

  const quizzes = myQuizzes
  const searchedQuizzes = useAdminSearch(quizzes, searchQuery)

  const handleFilterChange = (newStatus) => {
    setFilterStatus(newStatus)
    setCurrentPage(1)
  }

  const pendingCount = quizzes.filter((q) => q.status === 'pending').length
  const approvedCount = quizzes.filter((q) => q.status === 'approved').length
  const rejectedCount = quizzes.filter((q) => q.status === 'rejected').length

  const handleApprove = () => {
    toast.success('Квиз одобрен', {
      description: 'Эта функция еще не доработана',
    })
  }

  const handleRejectClick = (quiz) => {
    setSelectedQuiz(quiz)
    setIsRejectDialogOpen(true)
  }

  const handleViewClick = (quiz) => {
    setSelectedQuiz(quiz)
    setIsViewDialogOpen(true)
  }

  const handleRejectConfirm = () => {
    if (!selectedQuiz) return
    toast.success('Квиз отклонен', {
      description: 'Эта функция еще не доработана',
    })
    setIsRejectDialogOpen(false)
    setSelectedQuiz(null)
  }

  return (
    <div className={styles.adminPanel}>
      <div className={styles.container}>
        <AdminPanelHeader onBack={onBack} />

        <StatsCards
          pendingCount={pendingCount}
          approvedCount={approvedCount}
          rejectedCount={rejectedCount}
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
        />
      </div>

      <ViewQuizDialog
        isOpen={isViewDialogOpen}
        quiz={selectedQuiz}
        onClose={() => setIsViewDialogOpen(false)}
        onApprove={handleApprove}
        onRejectClick={handleRejectClick}
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
