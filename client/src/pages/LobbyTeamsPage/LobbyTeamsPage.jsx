import React from 'react'

import { LobbyTeams } from '@widgets'

export function LobbyTeamsPage() {
  const quiz = {
    title: 'Основы JavaScript',
    questionCount: 12,
    duration: 15,
    difficulty: 'Легкий',
  }

  return <LobbyTeams quiz={quiz} />
}
