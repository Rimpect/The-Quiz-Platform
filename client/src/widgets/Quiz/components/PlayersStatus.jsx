import { Avatar } from '@shared'
import { Crown, Check, Ban } from 'lucide-react'

import styles from './PlayersStatus.module.scss'

/**
 * Статус-бар игроков в командном квизе: по каждому видно —
 * капитан ли он, ответил ли на текущий вопрос, забанен и в сети ли.
 */
export function PlayersStatus({ players = [], teams = [] }) {
  if (!players.length) return null

  // Группируем игроков по командам (порядок — как в списке команд)
  const byTeam = teams.map((t) => ({
    id: t.id,
    name: t.name,
    members: players.filter((p) => p.team_id === t.id),
  }))
  const noTeam = players.filter((p) => !p.team_id)
  if (noTeam.length)
    byTeam.push({ id: '__none', name: 'Без команды', members: noTeam })

  return (
    <div className={styles.wrapper}>
      {byTeam.map((team) => (
        <div key={team.id} className={styles.team}>
          <span className={styles.teamName}>{team.name}</span>
          <div className={styles.players}>
            {team.members.map((p) => (
              <div
                key={p.user_id}
                className={`${styles.player} ${p.is_banned ? styles.banned : ''}`}
                title={p.nickname}
              >
                <span className={styles.avatarBox}>
                  <Avatar src={p.photo_profile} alt={p.nickname} size={28} />
                  <span
                    className={`${styles.dot} ${
                      p.online ? styles.online : styles.offline
                    }`}
                  />
                </span>
                <span className={styles.name}>{p.nickname}</span>
                {p.is_leader && (
                  <Crown size={14} className={styles.leaderIcon} />
                )}
                {p.is_banned ? (
                  <Ban size={14} className={styles.banIcon} />
                ) : (
                  p.answered_current && (
                    <Check size={14} className={styles.answeredIcon} />
                  )
                )}
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  )
}
