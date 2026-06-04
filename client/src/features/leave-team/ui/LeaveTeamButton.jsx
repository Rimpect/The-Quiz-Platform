import { Button } from '@shared'

export function LeaveTeamButton({ onClick }) {
  return (
    <Button variant="black" onClick={onClick}>
      Покинуть
    </Button>
  )
}
