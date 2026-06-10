import { Input } from '@shared'
import clsx from 'clsx'
import { Search } from 'lucide-react'

import styles from './SearchBar.module.scss'

export function SearchBar({
  value,
  onChange,
  placeholder = 'Поиск...',
  elevated = true,
}) {
  return (
    <div
      className={clsx(styles.searchCard, {
        [styles.elevated]: elevated,
        [styles.flat]: !elevated,
      })}
    >
      <div className={styles.searchWrapper}>
        <span className={styles.searchIcon}>
          <Search />
        </span>

        <Input
          type="text"
          placeholder={placeholder}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          maxLength={100}
          variant="search"
        />
      </div>
    </div>
  )
}
