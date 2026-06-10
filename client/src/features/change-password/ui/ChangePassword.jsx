import { useState } from 'react'

import { Button, Input } from '@shared'
import { toast } from 'sonner'

import { changePasswordSchema } from '../model/schema/changePasswordSchema'

import styles from './ChangePassword.module.scss'

export function ChangePassword() {
  const [currentPassword, setCurrentPassword] = useState('')
  const [newPassword, setNewPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [loading, setLoading] = useState(false)

  const handleChangePassword = async () => {
    // 1. Валидация через Zod
    const result = changePasswordSchema.safeParse({
      currentPassword,
      newPassword,
      confirmPassword,
    })

    if (!result.success) {
      const errors = result.error.flatten().fieldErrors

      const firstError = Object.values(result.error.flatten().fieldErrors)
        .flat()
        .find(Boolean)

      if (firstError) {
        toast.error(firstError)
        return
      }
      return
    }

    try {
      setLoading(true)

      // 2. MOCK логика (имитация бэка)
      await new Promise((resolve, reject) => {
        setTimeout(() => {
          // пример "неверного пароля"
          if (currentPassword !== '123') {
            reject(new Error('Неверный текущий пароль'))
          } else {
            resolve(true)
          }
        }, 800)
      })

      toast.success('Пароль успешно изменён')

      setCurrentPassword('')
      setNewPassword('')
      setConfirmPassword('')
    } catch (e) {
      toast.error(e.message || 'Ошибка изменения пароля')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className={styles.card}>
      <h2 className={styles.title}>Изменение пароля</h2>

      <div className={styles.field}>
        <label>Текущий пароль</label>
        <Input
          type="password"
          value={currentPassword}
          onChange={(e) => setCurrentPassword(e.target.value)}
        />
      </div>

      <div className={styles.field}>
        <label>Новый пароль</label>
        <Input
          type="password"
          value={newPassword}
          onChange={(e) => setNewPassword(e.target.value)}
        />
      </div>

      <div className={styles.field}>
        <label>Подтвердите пароль</label>
        <Input
          type="password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
        />
      </div>

      <Button
        variant="white"
        fullWidth
        onClick={handleChangePassword}
        disabled={loading}
      >
        {loading ? 'Сохранение...' : 'Изменить пароль'}
      </Button>
    </div>
  )
}
