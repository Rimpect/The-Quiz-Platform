import { useState } from 'react'

import { Button, Input } from '@shared'
import { client } from '@shared/api/client'
import { Eye, EyeOff } from 'lucide-react'
import { toast } from 'sonner'

import { changePasswordSchema } from '../model/schema/changePasswordSchema'

import styles from './ChangePassword.module.scss'

function PasswordField({ label, value, onChange }) {
  const [show, setShow] = useState(false)
  return (
    <div className={styles.field}>
      <label>{label}</label>
      <div style={{ position: 'relative' }}>
        <Input
          type={show ? 'text' : 'password'}
          value={value}
          onChange={onChange}
          style={{ paddingRight: '2.5rem' }}
        />
        <button
          type="button"
          onClick={() => setShow((s) => !s)}
          style={{
            position: 'absolute',
            right: '0.75rem',
            top: '50%',
            transform: 'translateY(-50%)',
            background: 'none',
            border: 'none',
            cursor: 'pointer',
            padding: 0,
            display: 'flex',
            alignItems: 'center',
            color: 'var(--color-text-secondary, #888)',
          }}
          tabIndex={-1}
        >
          {show ? <EyeOff size={18} /> : <Eye size={18} />}
        </button>
      </div>
    </div>
  )
}

export function ChangePassword() {
  const [currentPassword, setCurrentPassword] = useState('')
  const [newPassword, setNewPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [loading, setLoading] = useState(false)

  const handleChangePassword = async () => {
    const result = changePasswordSchema.safeParse({
      currentPassword,
      newPassword,
      confirmPassword,
    })

    if (!result.success) {
      const firstError = Object.values(result.error.flatten().fieldErrors)
        .flat()
        .find(Boolean)
      if (firstError) toast.error(firstError)
      return
    }

    try {
      setLoading(true)
      await client('/users/me/change-password', {
        method: 'POST',
        body: JSON.stringify({
          current_password: currentPassword,
          new_password: newPassword,
        }),
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

      <PasswordField
        label="Текущий пароль"
        value={currentPassword}
        onChange={(e) => setCurrentPassword(e.target.value)}
      />
      <PasswordField
        label="Новый пароль"
        value={newPassword}
        onChange={(e) => setNewPassword(e.target.value)}
      />
      <PasswordField
        label="Подтвердите пароль"
        value={confirmPassword}
        onChange={(e) => setConfirmPassword(e.target.value)}
      />

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
