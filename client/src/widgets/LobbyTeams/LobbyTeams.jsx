import { useLobbyTeams } from './model/useLobbyTeams'
import { PreLobby } from './ui/PreLobby'
import { TeamsRoom } from './ui/TeamsRoom'

export function LobbyTeams({ quiz, quizId }) {
  const lobby = useLobbyTeams(quizId)

  if (!lobby.sessionId) {
    return (
      <PreLobby
        quiz={quiz}
        loading={lobby.loading}
        onCreate={lobby.createLobby}
        onJoinByCode={lobby.joinByCode}
      />
    )
  }

  return <TeamsRoom quiz={quiz} lobby={lobby} />
}
