// ui/UserMenu.jsx
import { Button, ROUTES } from '@shared'
import { User } from 'lucide-react'
import { Link } from 'react-router-dom'
import { useCurrentUser } from '@shared/hooks/useCurrentUser'

import styles from './UserMenu.module.scss'

export function UserMenu() {
  const { user, isAuthenticated } = useCurrentUser()
  // const navigate = useNavigate()

  // const handleLogout = () => {
  //   localStorage.removeItem('user')
  //   navigate(ROUTES.main)
  //   window.location.reload()
  // }

  if (!isAuthenticated) {
    return (
      <div className={styles.user}>
        <User />
        <span>Гость</span>
        <Link to={ROUTES.login}>
          <Button variant="white" size="medium">
            Войти
          </Button>
        </Link>
      </div>
    )
  }

  return (
    <div className={styles.user}>
      {user?.avatar ? (
        <img src={user.avatar} alt={user.name} className={styles.avatar} />
      ) : (
        <User />
      )}
      <span>{user?.name}</span>

      <div className={styles.actions}>
        <Link to={ROUTES.profile}>
          <Button variant="white" size="medium">
            Профиль
          </Button>
        </Link>
        {/* <button onClick={handleLogout} className={styles.logoutButton}>
          <LogOut size={16} />
        </button> */}
      </div>
    </div>
  )
}
