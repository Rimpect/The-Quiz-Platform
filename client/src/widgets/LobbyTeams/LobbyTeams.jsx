import { useState } from 'react'

import { TeamCard, QuizInfoCard } from '@entities'
import { CreateTeamModal, LobbyTimer } from '@features'
import { Button } from '@shared'

import styles from './LobbyTeams.module.scss'

export function LobbyTeams({ quiz }) {
  const [selectedTeam, setSelectedTeam] = useState(null)
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [teams, setTeams] = useState([
    {
      id: 1,
      name: 'Команда Альфа',
      maxMembers: 10,
      members: [
        {
          id: '1',
          name: 'Максим',
          avatar: '',
          isLeader: true,
          isReady: true,
        },
      ],
    },
    {
      id: 2,
      name: 'Команда Бета',
      maxMembers: 10,
      members: [
        {
          id: '1',
          name: 'Максим',
          avatar: '',
          isLeader: true,
          isReady: true,
        },
      ],
    },
    {
      id: 3,
      name: 'Команда Гамма',
      maxMembers: 10,
      members: [
        {
          id: '1',
          name: 'Максим',
          avatar: '',
          isLeader: true,
          isReady: true,
        },
        {
          id: '2',
          name: 'Максим',
          avatar: '',
          isLeader: true,
          isReady: true,
        },
      ],
    },
  ])

  const currentMembers = teams.reduce(
    (acc, team) => acc + team.members.length,
    0,
  )

  const handleCreateTeam = (newTeam) => {
    const team = {
      id: Date.now(),
      name: newTeam.name,
      description: newTeam.description,
      maxMembers: 10,
      members: [
        {
          id: 'current-user-id',
          name: 'Вы',
          avatar: '',
          isLeader: true,
          isReady: false,
        },
      ],
    }
    setTeams([...teams, team])
  }

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h1>{quiz.title}</h1>
        <LobbyTimer
          initialTime={180}
          onTimeEnd={() => alert('Время вышло! Да начнутся игры!')}
        />
      </div>

      <div className={styles.content}>
        <div className={styles.teams}>
          <div className={styles.stats}>
            Команды: {teams.length} | Игроков: {currentMembers}
            <Button
              variant="black"
              onClick={() => setIsModalOpen(true)}
              className={styles.createButton}
            >
              Создать команду
            </Button>
          </div>

          {teams.map((team) => (
            <TeamCard
              key={team.id}
              team={team}
              selectedTeam={selectedTeam}
              onJoin={setSelectedTeam}
              onLeave={() => setSelectedTeam(null)}
            />
          ))}
        </div>

        <div className={styles.sidebar}>
          <QuizInfoCard quiz={quiz} />

          {selectedTeam && (
            <div className={styles.readySection}>
              <p>
                Вы в команде{' '}
                <strong>
                  {teams.find((team) => team.id === selectedTeam)?.name}
                </strong>
              </p>
              <p>Нажмите на кнопку "Готов", когда будете готовы начать</p>
              <Button variant="green" onClick={() => alert('Готов!')}>
                Готов
              </Button>
            </div>
          )}
        </div>
      </div>

      <CreateTeamModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onCreate={handleCreateTeam}
      />
    </div>
  )
}
