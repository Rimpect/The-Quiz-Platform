import { useState } from 'react'

import { RejectQuizDialog } from '../../shared/RejectQuizDialog/RejectQuizDialog'
import { ViewQuizDialog } from '../../shared/ViewQuizDialog/ViewQuizDialog'
import { AdminHeader } from '../../widgets/AdminHeader/AdminHeader'
import { QuizTabs } from '../../widgets/QuizTabs/QuizTabs'
import { SearchBar } from '../../widgets/SearchBar/SearchBar'
import { StatsCards } from '../../widgets/StatsCards/StatsCards'

import styles from './AdminPanel.module.scss'

export function AdminPanel({ onBack, quizzes = [], onApprove, onReject }) {
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedQuiz, setSelectedQuiz] = useState(null)
  const [isRejectDialogOpen, setIsRejectDialogOpen] = useState(false)
  const [isViewDialogOpen, setIsViewDialogOpen] = useState(false)
  const [filterStatus, setFilterStatus] = useState('pending')
  const [currentPage, setCurrentPage] = useState(1)

  const safeQuizzes = Array.isArray(quizzes) ? quizzes : []

  const filteredQuizzes = safeQuizzes.filter((quiz) => {
    const matchesSearch =
      quiz.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      quiz.author.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesStatus = filterStatus === 'all' || quiz.status === filterStatus
    return matchesSearch && matchesStatus
  })

  const pendingCount = safeQuizzes.filter((q) => q.status === 'pending').length
  const approvedCount = safeQuizzes.filter(
    (q) => q.status === 'approved',
  ).length
  const rejectedCount = safeQuizzes.filter(
    (q) => q.status === 'rejected',
  ).length

  const handleApprove = (quiz) => {
    onApprove(quiz.id)
    alert(`Квиз "${quiz.title}" одобрен`)
  }

  const handleRejectClick = (quiz) => {
    setSelectedQuiz(quiz)
    setIsRejectDialogOpen(true)
  }

  const handleViewClick = (quiz) => {
    setSelectedQuiz(quiz)
    setIsViewDialogOpen(true)
  }

  const handleRejectConfirm = (reason) => {
    if (!selectedQuiz) return
    onReject(selectedQuiz.id, reason)
    alert(`Квиз "${selectedQuiz.title}" отклонен`)
    setIsRejectDialogOpen(false)
    setSelectedQuiz(null)
  }

  return (
    <div className={styles.adminPanel}>
      <div className={styles.container}>
        <AdminHeader onBack={onBack} />

        <StatsCards
          pendingCount={pendingCount}
          approvedCount={approvedCount}
          rejectedCount={rejectedCount}
        />

        <SearchBar searchQuery={searchQuery} onSearchChange={setSearchQuery} />

        <QuizTabs
          quizzes={filteredQuizzes}
          filterStatus={filterStatus}
          onFilterChange={setFilterStatus}
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
