import { Button } from '@shared'

import styles from './TeamCard.module.scss'
import { TeamMember } from './TeamMember'

export function TeamCard({ team, selectedTeam, onJoin, onLeave }) {
  const isSelected = selectedTeam === team.id

  return (
    <div className={`${styles.card} ${isSelected ? styles.selected : ''}`}>
      <div className={styles.header}>
        <div>
          <h3>{team.name}</h3>

          <span>
            {team.members.length}/{team.maxMembers}
          </span>
        </div>

        {isSelected ? (
          <Button variant="white" onClick={onLeave}>
            Покинуть
          </Button>
        ) : (
          <Button variant="black" onClick={() => onJoin(team.id)}>
            Вступить
          </Button>
        )}
      </div>

      <div className={styles.members}>
        {team.members.map((member) => (
          <TeamMember key={member.id} member={member} />
        ))}
      </div>
    </div>
  )
}
