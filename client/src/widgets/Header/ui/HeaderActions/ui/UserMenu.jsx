import { Button, ROUTES } from '@shared'
import { User } from 'lucide-react'
import { Link } from 'react-router-dom'

import styles from './UserMenu.module.scss'

export function UserMenu() {
  return (
    <div>
      <div className={styles.user}>
        <User />
        <span>Имя пользователя/Гость</span>
        <Link to={ROUTES.profile}>
          <Button variant="white" size="medium">
            Войти
          </Button>
        </Link>
      </div>
    </div>
  )
}
