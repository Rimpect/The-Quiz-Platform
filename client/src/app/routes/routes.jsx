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
import { createHashRouter } from 'react-router-dom'

import { Layout } from '../../widgets/Layout/Layout.jsx'

export const routes = createHashRouter([
  {
    path: '/',
    element: <SignUpPage />,
  },
  {
    path: '/RegistrationPage',
    element: <RegistrationPage />,
  },
  {
    element: <Layout />,
    children: [
      {
        path: '/MainPage',
        element: <MainPage />,
      },
      {
        path: '/PersonalAccount',
        element: <PersonalAccount />,
      },
      {
        path: '/QuizDescription/:id',
        element: <QuizDescriptionPage />,
      },
      {
        path: '/ProfileSettingsPage',
        element: <ProfileSettingsPage />,
      },
      {
        path: '/AdminPanel',
        element: <AdminPanel />,
      },
      {
        path: '/CreateQuizPage',
        element: <CreateQuizPage />,
      },
    ],
  },
  {
    path: '/QuizPage/:id',
    element: <QuizPage />,
  },
  {
    path: '/FinishQuizPage/:id',
    element: <FinishQuizPage />,
  },
  {
    path: '/NotFoundPage',
    element: <NotFoundPage />,
  },
])
