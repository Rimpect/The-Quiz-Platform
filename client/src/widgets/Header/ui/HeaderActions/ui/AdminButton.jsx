import React from 'react'

import { Button, ROUTES } from '@shared'
import { Shield } from 'lucide-react'
import { Link } from 'react-router-dom'

import styles from './AdminButton.module.scss'

export function AdminButton() {
  return (
    <div>
      <Link to={ROUTES.admin}>
        <Button variant="white" size="medium" icon={<Shield size={20} />}>
          <span className={styles.label}>Админка</span>
        </Button>
      </Link>
    </div>
  )
}
