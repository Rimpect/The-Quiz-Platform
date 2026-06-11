import React, { useState, useEffect } from 'react'

import { Button, Input } from '@shared'
import { Save } from 'lucide-react'

import styles from './ProfileForm.module.scss'

export function ProfileForm({ user }) {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')

  useEffect(() => {
    if (!user) return

    setName(user.name || '')
    setEmail(user.email || '')
  }, [user])
  const handleSave = () => {
    // TODO: api request

    console.log({
      name,
      email,
    })

    alert('Профиль обновлен')
  }
  return (
    <div>
      <div className={styles.field}>
        <label>Имя</label>

        <Input
          type="text"
          value={name}
          maxLength={50}
          onChange={(e) => setName(e.target.value)}
        />
      </div>
      <div className={styles.field}>
        <label>Email</label>

        <Input
          type="email"
          value={email}
          maxLength={50}
          onChange={(e) => setEmail(e.target.value)}
        />
      </div>
      <Button variant="white" icon={<Save />} onClick={handleSave}>
        Сохранить изменения
      </Button>
    </div>
  )
}
