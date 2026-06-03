import { useAuthStore } from '@entities'
import { Button, ROUTES } from '@shared'
import { User, LogOut } from 'lucide-react'
import { Link, useNavigate } from 'react-router-dom'
import { toast } from 'sonner'

import styles from './UserMenu.module.scss'

export function UserMenu() {
  const user = useAuthStore((state) => state.user)
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated)
  const logout = useAuthStore((state) => state.logout)
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    toast.info('Вы вышли из аккаунта')
    console.log('after logout', useAuthStore.getState())
    navigate(ROUTES.main, { replace: true })
  }

  if (!isAuthenticated) {
    return (
      <div className={styles.user}>
        <User />
        <span>Гость</span>
        <Link to={ROUTES.auth}>
          <Button variant="white" size="medium">
            Войти
          </Button>
        </Link>
      </div>
    )
  }

  return (
    <div className={styles.user}>
      <User />
      <span>{user?.name}</span>

      <div className={styles.actions}>
        <Link to={ROUTES.profile}>
          <Button variant="white" size="medium">
            Профиль
          </Button>
        </Link>
        <Button
          variant="white"
          size="medium"
          onClick={handleLogout}
          className={styles.logoutButton}
        >
          <LogOut size={16} />
        </Button>
      </div>
    </div>
  )
}
