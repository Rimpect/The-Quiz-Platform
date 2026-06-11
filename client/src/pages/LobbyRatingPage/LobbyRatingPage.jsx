import { LobbyRating } from '@widgets'

export function LobbyRatingPage() {
  const quiz = {
    title: 'Основы JavaScript',
    questionCount: 12,
    duration: 15,
    difficulty: 'Легкий',
  }
  return <LobbyRating quiz={quiz} />
}
