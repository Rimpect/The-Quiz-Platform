import { useEffect, useState } from 'react'

import { client } from '@shared'
import { toast } from 'sonner'

/**
 * Логика диалога просмотра квиза (для админки): дозагрузка полного квиза
 * с вопросами/ответами и удаление с подтверждением.
 */
export function useViewQuizDialog(quiz, isOpen, { onClose, onDelete }) {
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

  return { fullQuiz, loading, confirmOpen, setConfirmOpen, deleting, handleDelete }
}
