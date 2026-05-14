import clsx from 'clsx'
import { Search } from 'lucide-react'

import styles from './SearchBar.module.scss'

export function SearchBar({ searchQuery, onSearchChange, elevated = true }) {
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
          placeholder="Поиск по названию или автору..."
          className={styles.searchInput}
          value={searchQuery}
          onChange={(e) => onSearchChange(e.target.value)}
        />
      </div>
    </div>
  )
}
