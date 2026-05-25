import { useState } from 'react'

import { Button, ROUTES } from '@shared'
import { useNavigate } from 'react-router-dom'
import { toast } from 'sonner'

import { deleteAccount } from '../api/deleteAccount'

import styles from './DangerZone.module.scss'

export function DangerZone() {
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()
  const handleDelete = async () => {
    try {
      setLoading(true)

      const response = await deleteAccount()

      toast.success(response.message)

      navigate(ROUTES.main)
      //   @TODO добавить потом еще на всякий случай логаут
    } catch (e) {
      toast.error(e.message || 'Что-то пошло не так')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className={styles.card}>
      <h2 className={styles.title}>Опасная зона</h2>

      <p className={styles.text}>
        После удаления аккаунта все данные будут потеряны.
      </p>

      <Button variant="red" fullWidth onClick={handleDelete} disabled={loading}>
        {loading ? 'Удаление...' : 'Удалить аккаунт'}
      </Button>
    </div>
  )
}
