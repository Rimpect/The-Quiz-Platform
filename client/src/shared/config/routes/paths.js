// const ROUTES = {
//   main: '/',
//   auth: '/auth',
//   register: '/RegistrationPage',
//   quiz: '/QuizPage/:id',
//   quizDescription: '/QuizDescription/:id',
//   finishQuiz: '/FinishQuizPage/:id',
//   profile: '/PersonalAccount',
//   settings: '/ProfileSettingsPage',
//   admin: '/AdminPanel',
//   createQuiz: '/CreateQuizPage',
//   notFound: '/NotFoundPage',
// }
// export { ROUTES }
// shared/config/routes.js
// shared/config/routes.js
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
}

// Функции для путей с ID
export const getQuizRoute = (id) => `${ROUTES.quiz}/${id}`
export const getQuizDescriptionRoute = (id) => `${ROUTES.quizDescription}/${id}`
export const getFinishQuizRoute = (id) => `${ROUTES.finishQuiz}/${id}`

export { ROUTES }
