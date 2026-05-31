import { ThemeToggle } from '@features'
import { useCurrentUser } from '@shared/hooks/useCurrentUser'

import styles from './HeaderActions.module.scss'
import { AdminButton, UserMenu } from './ui'

export function HeaderActions() {
  const { isAdmin } = useCurrentUser()

  return (
    <div className={styles.container}>
      {isAdmin && <AdminButton />}
      <ThemeToggle />
      <UserMenu />
    </div>
  )
}
