import { useEffect, useState } from 'react'

import { useUser } from '@entities'
import { ChangePassword, DangerZone, ProfileInfo } from '@features'
import { Button, ROUTES } from '@shared'
import { client } from '@shared/api/client'
import { Link } from 'react-router-dom'

import styles from './ProfileSettingsPage.module.scss'

export function ProfileSettingsPage() {
  const storeUser = useUser()
  const [email, setEmail] = useState('')

  useEffect(() => {
    client('/users/me')
      .then((data) => {
        if (data?.email) setEmail(data.email)
      })
      .catch(() => {})
  }, [])

  const user = {
    name: storeUser?.name || storeUser?.nickname || '',
    email,
  }

  return (
    <div className={styles.page}>
      <div className={styles.container}>
        <div className={styles.action}>
          <h1 className={styles.title}>Настройки профиля</h1>
          <Link to={ROUTES.profile}>
            <Button variant="white">Назад</Button>
          </Link>
        </div>
        <div className={styles.content}>
          <ProfileInfo user={user} />
          <ChangePassword />
          <DangerZone />
        </div>
      </div>
    </div>
  )
}
