import { useAuthStore } from '@entities'
import { client } from '@shared/api/client'
import { mediaService } from '@shared/api/services/mediaService'
import { toast } from 'sonner'

import { AvatarUploader } from './AvatarUploader'
import { ProfileForm } from './ProfileForm'
import styles from './ProfileInfo.module.scss'

export function ProfileInfo({ user }) {
  const setUser = useAuthStore((state) => state.setUser)
  const storeUser = useAuthStore((state) => state.user)

  const handleAvatarChange = async (_dataUrl, file) => {
    try {
      const res = await mediaService.uploadSimple('profile', file)
      await client('/users/me', {
        method: 'PUT',
        body: JSON.stringify({ photo_profile: res.url }),
      })
      // Обновляем юзера в сторе, чтобы аватар сразу обновился в шапке
      setUser({ ...storeUser, photo_profile: res.url })
      toast.success('Фото профиля обновлено')
    } catch (e) {
      toast.error(e.message || 'Не удалось обновить фото')
    }
  }

  return (
    <div className={styles.card}>
      <h2 className={styles.title}>Личная информация</h2>

      <AvatarUploader
        initialAvatar={user?.photo_profile || null}
        onAvatarChange={handleAvatarChange}
      />

      <ProfileForm user={user} />
    </div>
  )
}
