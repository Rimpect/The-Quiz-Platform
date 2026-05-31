import { ChangePassword, DangerZone, ProfileInfo } from '@features'

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
        <h1 className={styles.title}>Настройки профиля</h1>

        <div className={styles.content}>
          <ProfileInfo user={mockUser} />

          <ChangePassword />

          <DangerZone />
        </div>
      </div>
    </div>
  )
}
