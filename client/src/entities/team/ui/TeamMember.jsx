import { Crown, CheckCircle } from 'lucide-react'

import styles from './TeamMember.module.scss'

export function TeamMember({ member }) {
  return (
    <div className={styles.member}>
      <div className={styles.avatar}>{member.name[0]}</div>

      <span>{member.name}</span>

      {member.isLeader && <Crown size={14} className={styles.leaderIcon} />}

      {member.isReady && <CheckCircle size={14} className={styles.readyIcon} />}
    </div>
  )
}
