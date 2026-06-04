import {
  AdminPanel,
  FinishQuizPage,
  MainPage,
  PersonalAccount,
  ProfileSettingsPage,
  QuizDescriptionPage,
  QuizPage,
  SignInPage,
  RegistrationPage,
  CreateQuizPage,
  NotFoundPage,
  LobbyRatingPage,
  LobbyTeamsPage,
  LeaderboardRatingPage,
} from '@pages'
import { ROUTES } from '@shared'
import { createHashRouter, Navigate } from 'react-router-dom'

import { Layout } from '../../widgets/Layout/Layout.jsx'

import { AppGuard } from './AppGuard.jsx'

export const router = createHashRouter([
  {
    path: ROUTES.auth,
    element: <SignInPage />,
  },
  {
    path: ROUTES.register,
    element: <RegistrationPage />,
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
    ],
  },
  {
    element: <Layout />,
    children: [
      {
        path: ROUTES.main,
        element: <MainPage />,
      },
      {
        path: `${ROUTES.quizDescription}/:id`,
        element: <QuizDescriptionPage />,
      },
    ],
  },
  {
    path: `${ROUTES.quiz}/:id`,
    element: <QuizPage />,
  },
  {
    path: `${ROUTES.finishQuiz}/:id`,
    element: <FinishQuizPage />,
  },
  {
    path: ROUTES.notFound,
    element: <NotFoundPage />,
  },
  {
    path: ROUTES.leaderboardRating,
    element: <LeaderboardRatingPage />,
  },
  {
    path: ROUTES.lobbyTeams,
    element: <LobbyTeamsPage />,
  },
  {
    path: ROUTES.lobbyRating,
    element: <LobbyRatingPage />,
  },
  {
    path: '*',
    element: <Navigate to={ROUTES.notFound} replace />,
  },
])
