import { Button } from '@shared'

export function JoinTeamButton({ team, onClick }) {
  const isFull = team.members.length >= team.maxMembers

  return (
    <Button variant="white" disabled={isFull} onClick={onClick}>
      {isFull ? 'Заполнено' : 'Присоединиться'}
    </Button>
  )
}
