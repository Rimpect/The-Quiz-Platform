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

        <input
          type="text"
          placeholder={placeholder}
          className={styles.searchInput}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          maxLength={100}
        />
      </div>
    </div>
  )
}
