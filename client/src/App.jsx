import './App.scss'
import { Routes, Route } from 'react-router-dom'

import { FinishQuiz } from './pages/FinishQuiz/FinishQuiz'
import { MainPage } from './pages/MainPage/MainPage'
import { PersonalAccount } from './pages/PersonalAccount/PersonalAccount'
import { QuizDescriptionPage } from './pages/QuizDescriptionPage/QuizDescriptionPage.jsx'
import { QuizPage } from './pages/QuizPage/QuizPage'
import { RegistrationPage } from './pages/RegistrationPage/RegistrationPage.jsx'
import { SignUp } from './pages/SignUp/SignUp.jsx'
import { Layout } from './widgets/Layout/Layout.jsx'

function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/MainPage" element={<MainPage />} />
        <Route path="/PersonalAccount" element={<PersonalAccount />} />
        <Route path="/QuizDescription/:id" element={<QuizDescriptionPage />} />
        {/* <Route path="/CreateQuiz" element={<CreateQuiz />} /> */}
      </Route>
      <Route path="/" element={<SignUp />} />
      <Route path="/RegistrationPage" element={<RegistrationPage />} />
      <Route path="/QuizPage/:id" element={<QuizPage />} />
      <Route path="/FinishQuiz/:id" element={<FinishQuiz />} />
    </Routes>
  )
}

export default App
