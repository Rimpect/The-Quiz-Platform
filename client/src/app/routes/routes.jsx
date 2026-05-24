import {
  AdminPanel,
  FinishQuizPage,
  MainPage,
  PersonalAccount,
  ProfileSettingsPage,
  QuizDescriptionPage,
  QuizPage,
  RegistrationPage,
  SignUpPage,
  CreateQuizPage,
  NotFoundPage,
} from '@pages'
import { ROUTES } from '@shared'
import { createHashRouter } from 'react-router-dom'

import { Layout } from '../../widgets/Layout/Layout.jsx'

export const router = createHashRouter([
  {
    path: ROUTES.auth,
    element: <SignUpPage />,
  },
  {
    path: ROUTES.register,
    element: <RegistrationPage />,
  },
  {
    element: <Layout />,
    children: [
      {
        path: ROUTES.main,
        element: <MainPage />,
      },
      {
        path: ROUTES.profile,
        element: <PersonalAccount />,
      },
      {
        path: ROUTES.quizDescription,
        element: <QuizDescriptionPage />,
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
])
