import { ThemeToggle } from '@features'

import styles from './HeaderActions.module.scss'
import { AdminButton } from './ui/AdminButton'
import { UserMenu } from './ui/UserMenu'

export function HeaderActions() {
  return (
    <div className={styles.container}>
      {/* @TODO сделать потом для кнопки с админкой сокрытие если пользовать не является админом! и так же для UserMenu доработать вариант с авторизованым и неавторизованым пользователем */}
      <AdminButton />
      <ThemeToggle />
      <UserMenu />
    </div>
  )
}
