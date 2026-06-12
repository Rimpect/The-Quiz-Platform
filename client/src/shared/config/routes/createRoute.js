import {
  getQuizRoute,
  getQuizDescriptionRoute,
  getFinishQuizRoute,
  getLobbyRatingRoute,
  getLobbyTeamsRoute,
  getLeaderboardRatingRoute,
} from './paths'

export const createRoute = {
  quiz: getQuizRoute,
  quizDescription: getQuizDescriptionRoute,
  finishQuiz: getFinishQuizRoute,
  lobbyRating: getLobbyRatingRoute,
  lobbyTeams: getLobbyTeamsRoute,
  leaderboardRating: getLeaderboardRatingRoute,
}
