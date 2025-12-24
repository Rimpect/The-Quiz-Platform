import "./App.css";
import { Routes, Route } from "react-router-dom";
import { MainPage } from "./pages/MainPage/MainPage";
import { QuizPage } from "./pages/QuizPage/QuizPage";
import { PersonalAccount } from "./pages/PersonalAccount/PersonalAccount";
import { SignUp } from "./pages/SignUp/SignUp.jsx";
import { Layout } from "./widgets/Layout/Layout.jsx";
import { QuizDescriptionPage } from "./pages/QuizDescriptionPage/QuizDescriptionPage.jsx";
function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<MainPage />} />
        <Route path="/quiz/:id" element={<QuizPage />} />
        <Route path="/PersonalAccount" element={<PersonalAccount />} />
        <Route path="/SignUp" element={<SignUp />} />
        <Route path="/QuizDescription/:id" element={<QuizDescriptionPage />} />
      </Route>
    </Routes>
  );
}

export default App;
