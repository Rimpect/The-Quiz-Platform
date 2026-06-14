import { useState } from 'react'

import { Button, Input } from '@shared'
import { Eye, EyeOff } from 'lucide-react'
import { toast } from 'sonner'

import { useChangePassword } from '../model/useChangePassword'

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
  const { submit, loading } = useChangePassword()

  const handleChangePassword = async () => {
    const res = await submit({ currentPassword, newPassword, confirmPassword })

    if (!res.ok) {
      // ошибки валидации (zod) либо сообщение сервера
      const firstError = res.errors
        ? Object.values(res.errors).flat().find(Boolean)
        : res.error
      toast.error(firstError || 'Ошибка изменения пароля')
      return
    }

    toast.success('Пароль успешно изменён')
    setCurrentPassword('')
    setNewPassword('')
    setConfirmPassword('')
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
