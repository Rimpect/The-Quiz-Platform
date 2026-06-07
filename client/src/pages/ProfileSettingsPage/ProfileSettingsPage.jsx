import { ChangePassword, DangerZone, ProfileInfo } from '@features'
import { Button, ROUTES } from '@shared'
import { Link } from 'react-router-dom'

import styles from './ProfileSettingsPage.module.scss'

const mockUser = {
  name: 'Максим',
  email: 'example@gmail.com',
  // avatar: '',
}

export function ProfileSettingsPage() {
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
          <ProfileInfo user={mockUser} />

          <ChangePassword />

          <DangerZone />
        </div>
      </div>
    </div>
  )
}
