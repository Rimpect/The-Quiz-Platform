import { lazy, Suspense } from 'react'

import { ROUTES } from '@shared'
import { createBrowserRouter, Navigate } from 'react-router-dom'

import { Layout } from '../../widgets/Layout/Layout.jsx'

import { AppGuard } from './AppGuard.jsx'

const lazyPage = (loader, name) =>
  lazy(() => loader().then((m) => ({ default: m[name] })))

const SignInPage = lazyPage(
  () => import('@pages/SignInPage/SignInPage'),
  'SignInPage',
)
const RegistrationPage = lazyPage(
  () => import('@pages/RegistrationPage/RegistrationPage'),
  'RegistrationPage',
)
const MainPage = lazyPage(() => import('@pages/MainPage/MainPage'), 'MainPage')
const PersonalAccount = lazyPage(
  () => import('@pages/PersonalAccount/PersonalAccount'),
  'PersonalAccount',
)
const ProfileSettingsPage = lazyPage(
  () => import('@pages/ProfileSettingsPage/ProfileSettingsPage'),
  'ProfileSettingsPage',
)
const AdminPanel = lazyPage(
  () => import('@pages/AdminPanel/AdminPanel'),
  'AdminPanel',
)
const CreateQuizPage = lazyPage(
  () => import('@pages/CreateQuizPage/CreateQuizPage'),
  'CreateQuizPage',
)
const QuizDescriptionPage = lazyPage(
  () => import('@pages/QuizDescriptionPage/QuizDescriptionPage'),
  'QuizDescriptionPage',
)
const QuizPage = lazyPage(() => import('@pages/QuizPage/QuizPage'), 'QuizPage')
const FinishQuizPage = lazyPage(
  () => import('@pages/FinishQuizPage/FinishQuizPage'),
  'FinishQuizPage',
)
const LeaderboardRatingPage = lazyPage(
  () => import('@pages/LeaderboardRatingPage/LeaderboardRatingPage'),
  'LeaderboardRatingPage',
)
const LobbyRatingPage = lazyPage(
  () => import('@pages/LobbyRatingPage/LobbyRatingPage'),
  'LobbyRatingPage',
)
const LobbyTeamsPage = lazyPage(
  () => import('@pages/LobbyTeamsPage/LobbyTeamsPage'),
  'LobbyTeamsPage',
)
const NotFoundPage = lazyPage(
  () => import('@pages/NotFoundPage/NotFoundPage'),
  'NotFoundPage',
)

const fallback = (
  <div style={{ padding: '2rem', textAlign: 'center' }}>Загрузка…</div>
)

const s = (element) => <Suspense fallback={fallback}>{element}</Suspense>

export const router = createBrowserRouter(
  [
    {
      path: ROUTES.auth,
      element: s(<SignInPage />),
    },
    {
      path: ROUTES.register,
      element: s(<RegistrationPage />),
    },
    {
      element: (
        <AppGuard>
          <Layout />
        </AppGuard>
      ),
      children: [
        {
          path: ROUTES.profile,
          element: <PersonalAccount />,
        },
        {
          path: ROUTES.settings,
          element: <ProfileSettingsPage />,
        },
        {
          path: ROUTES.admin,
          element: <AdminPanel />,
        },
        {
          path: ROUTES.createQuiz,
          element: <CreateQuizPage />,
        },
        {
          path: `${ROUTES.leaderboardRating}/:quizId`,
          element: <LeaderboardRatingPage />,
        },
        {
          path: `${ROUTES.lobbyTeams}/:quizId`,
          element: <LobbyTeamsPage />,
        },
        {
          path: `${ROUTES.lobbyRating}/:id`,
          element: <LobbyRatingPage />,
        },
      ],
    },
    {
      element: <Layout />,
      children: [
        {
          index: ROUTES.main,
          element: <MainPage />,
        },
        {
          path: `${ROUTES.quizDescription}/:id`,
          element: <QuizDescriptionPage />,
        },
      ],
    },
    {
      path: `${ROUTES.quiz}/:quizId/lobby`,
      element: s(<LobbyTeamsPage />),
    },
    {
      path: `${ROUTES.quiz}/:id`,
      element: s(<QuizPage />),
    },
    {
      path: `${ROUTES.finishQuiz}/:id`,
      element: s(<FinishQuizPage />),
    },
    {
      path: ROUTES.notFound,
      element: s(<NotFoundPage />),
    },
    {
      path: '*',
      element: <Navigate to={ROUTES.notFound} replace />,
    },
  ],
  {
    basename: import.meta.env.BASE_URL.replace(/\/+$/, '') || '/',
  },
)
