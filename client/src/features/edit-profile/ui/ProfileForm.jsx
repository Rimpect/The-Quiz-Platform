import React, { useState, useEffect } from 'react'

import { Button, Input } from '@shared'
import { client } from '@shared/api/client'
import { Save } from 'lucide-react'
import { toast } from 'sonner'

import styles from './ProfileForm.module.scss'

export function ProfileForm({ user }) {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (!user) return
    setName(user.name || '')
    setEmail(user.email || '')
  }, [user])

  const handleSave = async () => {
    try {
      setLoading(true)
      await client('/users/me', {
        method: 'PUT',
        body: JSON.stringify({ nickname: name, email }),
      })
      toast.success('Профиль обновлён')
    } catch (e) {
      toast.error(e.message || 'Ошибка сохранения')
    } finally {
      setLoading(false)
    }
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
      <Button
        variant="white"
        icon={<Save />}
        onClick={handleSave}
        disabled={loading}
      >
        {loading ? 'Сохранение...' : 'Сохранить изменения'}
      </Button>
    </div>
  )
}
