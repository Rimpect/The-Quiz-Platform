const ROUTES = {
  main: '/',
  auth: '/auth',
  register: '/register',
  quiz: '/quiz',
  quizDescription: '/quizDescription',
  finishQuiz: '/finishQuiz',
  profile: '/profile',
  settings: '/settings',
  admin: '/admin',
  createQuiz: '/createQuiz',
  notFound: '/notFound',
  leaderboardRating: '/leaderboardRating',
  lobbyRating: '/lobbyRating',
  lobbyTeams: '/lobbyTeams',
}

export const getQuizRoute = (id) => `${ROUTES.quiz}/${id}`
export const getQuizDescriptionRoute = (id) => `${ROUTES.quizDescription}/${id}`
export const getFinishQuizRoute = (id) => `${ROUTES.finishQuiz}/${id}`
export const getLobbyRatingRoute = (id) => `${ROUTES.lobbyRating}/${id}`
export const getLobbyTeamsRoute = (id) => `${ROUTES.lobbyTeams}/${id}`
export const getLeaderboardRatingRoute = (id) =>
  `${ROUTES.leaderboardRating}/${id}`
export { ROUTES }
