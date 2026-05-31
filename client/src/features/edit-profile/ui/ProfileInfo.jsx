import { AvatarUploader } from './AvatarUploader'
import { ProfileForm } from './ProfileForm'
import styles from './ProfileInfo.module.scss'

export function ProfileInfo({ user }) {
  return (
    <div className={styles.card}>
      <h2 className={styles.title}>Личная информация</h2>

      <AvatarUploader user={user} />

      <ProfileForm />
    </div>
  )
}
