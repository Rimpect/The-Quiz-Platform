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

import { ProtectedRoute } from './ProtectedRoute.jsx'
import { PublicRoute } from './PublicRoute.jsx'

export const router = createHashRouter([
  // Публичные маршруты (для неавторизованных)
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
    element: <Layout />,
    children: [
      {
        path: ROUTES.main,
        element: <MainPage />,
      },
      {
        path: ROUTES.quizDescription,
        element: <QuizDescriptionPage />,
      },
    ],
  },

  // Защищенные маршруты (с Layout)
  {
    element: <Layout />,
    children: [
      {
        path: ROUTES.profile,
        element: (
          <ProtectedRoute>
            <PersonalAccount />
          </ProtectedRoute>
        ),
      },

      {
        path: ROUTES.settings,
        element: (
          <ProtectedRoute>
            <ProfileSettingsPage />
          </ProtectedRoute>
        ),
      },
      {
        path: ROUTES.admin,
        element: (
          <ProtectedRoute requireAdmin>
            <AdminPanel />
          </ProtectedRoute>
        ),
      },
      {
        path: ROUTES.createQuiz,
        element: (
          <ProtectedRoute>
            <CreateQuizPage />
          </ProtectedRoute>
        ),
      },
    ],
  },

  // Публичные маршруты без Layout
  {
    path: ROUTES.quiz,
    element: <QuizPage />,
  },
  {
    path: ROUTES.finishQuiz,
    element: <FinishQuizPage />,
  },

  // 404 страница
  {
    path: ROUTES.notFound,
    element: <NotFoundPage />,
  },

  // Все неизвестные пути -> 404
  {
    path: '*',
    element: <Navigate to={ROUTES.notFound} replace />,
  },
])
