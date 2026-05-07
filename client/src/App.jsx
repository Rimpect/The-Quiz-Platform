import './App.scss'
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
} from '@pages'
import { Routes, Route } from 'react-router-dom'

import { Layout } from './widgets/Layout/Layout.jsx'

function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/MainPage" element={<MainPage />} />
        <Route path="/PersonalAccount" element={<PersonalAccount />} />
        <Route path="/QuizDescription/:id" element={<QuizDescriptionPage />} />
        <Route path="/ProfileSettingsPage" element={<ProfileSettingsPage />} />
        <Route path="/AdminPanel/" element={<AdminPanel />} />

        {/* <Route path="/CreateQuiz" element={<CreateQuiz />} /> */}
      </Route>
      <Route path="/" element={<SignUpPage />} />
      <Route path="/RegistrationPage" element={<RegistrationPage />} />
      <Route path="/QuizPage/:id" element={<QuizPage />} />
      <Route path="/FinishQuizPage/:id" element={<FinishQuizPage />} />
    </Routes>
  )
}

export default App
