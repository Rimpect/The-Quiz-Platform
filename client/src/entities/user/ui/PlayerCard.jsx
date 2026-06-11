import React from 'react'

import { CircleCheckBig } from 'lucide-react'

import styles from './PlayerCard.module.scss'

export function PlayerCard({ player, isReady }) {
  return (
    <div
      className={`${styles.card} ${isReady ? styles.ready : styles.waiting}`}
    >
      <div className={styles.avatar}>
        {player.avatar ? (
          <img src={player.avatar} alt={player.name} />
        ) : (
          <span className={styles.avatarPlaceholder}></span>
        )}
      </div>

      <div className={styles.info}>
        <div className={styles.name}>{player.name}</div>
        <div className={styles.status}>
          {isReady ? (
            <span className={styles.readyText}>Готов</span>
          ) : (
            <span className={styles.waitingText}>Ожидание...</span>
          )}
        </div>
      </div>

      <div className={styles.iconWrapper}>
        {isReady && <CircleCheckBig size={32} className={styles.checkIcon} />}
      </div>
    </div>
  )
}
