import { useAuthStore } from '@entities'

import styles from './HeaderActions.module.scss'
import { AdminButton, UserMenu } from './ui'

export function HeaderActions() {
  const isAdmin = useAuthStore((state) => state.user?.role === 'admin')

  return (
    <div className={styles.container}>
      {isAdmin && <AdminButton />}
      <UserMenu />
    </div>
  )
}
