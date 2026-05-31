import React from 'react'

import styles from './AchievementsTab.module.scss'

export function AchievementsTab({ achievements }) {
  return (
    <div>
      <div className={styles.tabContent}>
        <div className={styles.tabHeader}>
          <h2 className={styles.tabTitle}>
            Достижения ({achievements.filter((a) => a.unlocked).length}/
            {achievements.length})
          </h2>
        </div>
        <div className={styles.achievementsGrid}>
          {achievements.map((achievement, index) => (
            <div
              key={index}
              className={`${styles.achievementCard} ${
                achievement.unlocked ? styles.unlocked : styles.locked
              }`}
            >
              <div className={styles.achievementIcon}>{achievement.icon}</div>
              <h3 className={styles.achievementTitle}>{achievement.title}</h3>
              <p className={styles.achievementDescription}>
                {achievement.description}
              </p>
              {achievement.unlocked && (
                <div className={styles.achievementUnlocked}>✓ Получено</div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
