import { useState } from 'react'

import { Button } from '@shared'

import styles from './ChangePassword.module.scss'

export function ChangePassword() {
  const [currentPassword, setCurrentPassword] = useState('')

  const [newPassword, setNewPassword] = useState('')

  const [confirmPassword, setConfirmPassword] = useState('')

  const handleChangePassword = () => {
    // TODO: api request

    console.log({
      currentPassword,
      newPassword,
      confirmPassword,
    })

    alert('Пароль изменен')
  }

  return (
    <div className={styles.card}>
      <h2 className={styles.title}>Изменение пароля</h2>

      <div className={styles.field}>
        <label>Текущий пароль</label>

        <input
          type="password"
          value={currentPassword}
          onChange={(e) => setCurrentPassword(e.target.value)}
        />
      </div>

      <div className={styles.field}>
        <label>Новый пароль</label>

        <input
          type="password"
          value={newPassword}
          onChange={(e) => setNewPassword(e.target.value)}
        />
      </div>

      <div className={styles.field}>
        <label>Подтвердите пароль</label>

        <input
          type="password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
        />
      </div>
      <Button variant="white" fullWidth onClick={handleChangePassword}>
        Изменить пароль
      </Button>
    </div>
  )
}
