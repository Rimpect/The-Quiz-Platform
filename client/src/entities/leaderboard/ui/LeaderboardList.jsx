import { LeaderboardItem } from './LeaderboardItem'
import styles from './LeaderboardList.module.css'
export function LeaderboardList({ items }) {
  return (
    <div className={styles.list}>
      {items.map((item) => (
        <LeaderboardItem key={item.place} {...item} />
      ))}
    </div>
  )
}
