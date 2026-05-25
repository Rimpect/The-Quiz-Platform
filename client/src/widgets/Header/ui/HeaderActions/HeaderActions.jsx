import React from 'react'

import { ThemeToggle } from '@features'

import { AdminButton } from './ui/AdminButton'
import { UserMenu } from './ui/UserMenu'
import styles from './HeaderActions.module.scss'
export function HeaderActions() {
  return (
    <div className={styles.container}>
      <AdminButton />
      <ThemeToggle />
      <UserMenu />
    </div>
  )
}
