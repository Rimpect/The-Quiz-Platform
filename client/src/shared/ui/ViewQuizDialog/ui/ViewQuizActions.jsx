import { Button } from '@shared'
import { Eye, Check, X, Trash2 } from 'lucide-react'
import { useNavigate } from 'react-router-dom'

import styles from '../ViewQuizDialog.module.scss'

export function ViewQuizActions({
  quiz,
  onApprove,
  onRejectClick,
  onDeleteClick,
  onClose,
}) {
  const navigate = useNavigate()

  return (
    <div className={styles.viewActions}>
      {quiz.status === 'pending' && (
        <>
          <Button
            variant="green"
            fullWidth
            icon={<Check size={18} />}
            onClick={() => onApprove(quiz)}
          >
            Одобрить
          </Button>
          <Button
            variant="red"
            fullWidth
            icon={<X size={18} />}
            onClick={() => onRejectClick(quiz)}
          >
            Отклонить
          </Button>
        </>
      )}

      <Button
        variant="red"
        fullWidth
        icon={<Trash2 size={18} />}
        onClick={onDeleteClick}
      >
        Удалить
      </Button>

      <Button
        variant="transparent"
        fullWidth
        icon={<Eye size={18} />}
        onClick={() => {
          onClose()
          navigate(`/quiz/${quiz.id}`)
        }}
      >
        Посмотреть на сайте
      </Button>
    </div>
  )
}
