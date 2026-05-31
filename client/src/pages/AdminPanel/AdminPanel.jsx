import { useState } from 'react'

import { QuizSearch } from '@features'
import { RejectQuizDialog, ViewQuizDialog } from '@shared'
import { AdminPanelHeader, QuizTabs, StatsCards } from '@widgets'
import { toast } from 'sonner'

import styles from './AdminPanel.module.scss'

export function AdminPanel({
  onBack,
  quizzes = [], //onApprove, onReject
}) {
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedQuiz, setSelectedQuiz] = useState(null)
  const [isRejectDialogOpen, setIsRejectDialogOpen] = useState(false)
  const [isViewDialogOpen, setIsViewDialogOpen] = useState(false)
  const [filterStatus, setFilterStatus] = useState('pending')
  const [currentPage, setCurrentPage] = useState(1)

  const filteredQuizzes = quizzes.filter((quiz) => {
    const matchesSearch =
      quiz.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      quiz.author.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesStatus = filterStatus === 'all' || quiz.status === filterStatus
    return matchesSearch && matchesStatus
  })

  const handleFilterChange = (newStatus) => {
    setFilterStatus(newStatus)
    setCurrentPage(1)
  }

  const pendingCount = quizzes.filter((q) => q.status === 'pending').length
  const approvedCount = quizzes.filter((q) => q.status === 'approved').length
  const rejectedCount = quizzes.filter((q) => q.status === 'rejected').length

  // const handleApprove = (quiz) => {
  //   onApprove(quiz.id)
  //   alert(`Квиз "${quiz.title}" одобрен`)
  // }
  const handleApprove = () => {
    toast.success('Квиз одобрен', {
      description: 'Эта функция еще не доработана',
    })
  } //@TODO заглушка пока что вместо алертов будут кастомные модалки
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
    setSelectedQuiz(null) //@TODO заглушка пока что вместо алертов будут кастомные модалки
  }
  // const handleRejectConfirm = (reason) => {
  //   if (!selectedQuiz) return
  //   onReject(selectedQuiz.id, reason)
  //   alert(`Квиз "${selectedQuiz.title}" отклонен`)
  //   setIsRejectDialogOpen(false)
  //   setSelectedQuiz(null)
  // }
  return (
    <div className={styles.adminPanel}>
      <div className={styles.container}>
        <AdminPanelHeader onBack={onBack} />

        <StatsCards
          pendingCount={pendingCount}
          approvedCount={approvedCount}
          rejectedCount={rejectedCount}
        />

        <QuizSearch quizzes={quizzes} />

        <QuizTabs
          quizzes={filteredQuizzes}
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
