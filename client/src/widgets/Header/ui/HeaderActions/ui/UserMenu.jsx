import { useAuthStore } from '@entities'
import { Button, ROUTES, Avatar } from '@shared'
import { LogOut } from 'lucide-react'
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
    navigate(ROUTES.main, { replace: true })
  }

  if (!isAuthenticated) {
    return (
      <div className={styles.user}>
        <Avatar size={36} />
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
      <Avatar src={user?.photo_profile} alt={user?.nickname} size={36} />
      <span>{user?.nickname || user?.name}</span>

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
          aria-label="Выйти из аккаунта"
          title="Выйти из аккаунта"
        >
          <LogOut size={16} />
        </Button>
      </div>
    </div>
  )
}
