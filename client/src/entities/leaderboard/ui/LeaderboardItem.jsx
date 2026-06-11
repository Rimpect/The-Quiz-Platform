import { Crown, Medal } from 'lucide-react'

import styles from './LeaderboardItem.module.scss'

const PLACE_COLORS = {
  1: '#FFD700',
  2: '#C0C0C0',
  3: '#CD7F32',
}

const PLACE_CLASSES = {
  1: styles.gold,
  2: styles.silver,
  3: styles.bronze,
}

export function LeaderboardItem({ place, name, avatar, percent, time }) {
  const itemClass = PLACE_CLASSES[place] || styles.default

  const renderPlaceIcon = () => {
    switch (place) {
      case 1:
        return <Crown size={22} color={PLACE_COLORS[1]} />

      case 2:
        return <Medal size={22} color={PLACE_COLORS[2]} />

      case 3:
        return <Medal size={22} color={PLACE_COLORS[3]} />

      default:
        return <span className={styles.placeNumber}>#{place}</span>
    }
  }

  return (
    <div className={styles.wrapper}>
      <div className={`${styles.item} ${itemClass}`}>
        <div className={styles.left}>
          <div className={styles.placeIcon}>{renderPlaceIcon()}</div>

          <img src={avatar} alt={name} className={styles.avatar} />

          <span className={styles.name}>{name}</span>
        </div>

        <div className={styles.right}>
          <span className={styles.percent}>{percent}%</span>

          <span className={styles.time}>{time}</span>
        </div>
      </div>
    </div>
  )
}
