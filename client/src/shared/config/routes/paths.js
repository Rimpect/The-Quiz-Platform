const ROUTES = {
  main: '/',
  auth: '/auth',
  register: '/RegistrationPage',
  quiz: '/QuizPage',
  quizDescription: '/QuizDescription',
  finishQuiz: '/FinishQuizPage',
  profile: '/PersonalAccount',
  settings: '/ProfileSettingsPage',
  admin: '/AdminPanel',
  createQuiz: '/CreateQuizPage',
  notFound: '/NotFoundPage',
  leaderboardRating: '/LeaderboardRatingPage',
  lobbyRating: '/LobbyRatingPage',
  lobbyTeams: '/LobbyTeamsPage',
}

// Функции для путей с ID
export const getQuizRoute = (id) => `${ROUTES.quiz}/${id}`
export const getQuizDescriptionRoute = (id) => `${ROUTES.quizDescription}/${id}`
export const getFinishQuizRoute = (id) => `${ROUTES.finishQuiz}/${id}`
export const getLobbyRatingRoute = (id) => `${ROUTES.lobbyRating}/${id}`
export const getLobbyTeamsRoute = (id) => `${ROUTES.lobbyTeams}/${id}`
export const getLeaderboardRatingRoute = (id) =>
  `${ROUTES.leaderboardRating}/${id}`
export { ROUTES }
