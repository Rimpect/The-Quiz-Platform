import {
  AdminPanel,
  FinishQuizPage,
  MainPage,
  PersonalAccount,
  ProfileSettingsPage,
  QuizDescriptionPage,
  QuizPage,
  SignUpPage,
  CreateQuizPage,
  NotFoundPage,
} from '@pages'
import { ROUTES } from '@shared'
import { createHashRouter, Navigate } from 'react-router-dom'

import { Layout } from '../../widgets/Layout/Layout.jsx'

import { AppGuard } from './AppGuard.jsx'
import { PublicRoute } from './PublicRoute.jsx'

export const router = createHashRouter([
  {
    path: ROUTES.auth,
    element: (
      <PublicRoute>
        <SignUpPage />
      </PublicRoute>
    ),
  },
  {
    path: ROUTES.register,
    element: (
      <PublicRoute>
        <SignUpPage />
      </PublicRoute>
    ),
  },
  {
    element: (
      <AppGuard>
        <Layout />
      </AppGuard>
    ),
    children: [
      {
        path: ROUTES.main,
        element: <MainPage />,
      },

      {
        path: ROUTES.quizDescription,
        element: <QuizDescriptionPage />,
      },

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
    path: ROUTES.quiz,
    element: <QuizPage />,
  },
  {
    path: ROUTES.finishQuiz,
    element: <FinishQuizPage />,
  },
  {
    path: ROUTES.notFound,
    element: <NotFoundPage />,
  },

  {
    path: '*',
    element: <Navigate to={ROUTES.notFound} replace />,
  },
])
