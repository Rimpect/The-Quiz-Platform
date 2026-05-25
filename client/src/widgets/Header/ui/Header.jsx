import styles from './Header.module.scss'
import { HeaderActions } from './HeaderActions/HeaderActions'
import { HeaderLogo } from './HeaderLogo/HeaderLogo'

export function Header() {
  return (
    <div className={styles.container}>
      <HeaderLogo />
      <HeaderActions />
    </div>
  )
}
