// фичи для ProfileSettingsPage
export { ChangePassword } from './change-password'
export { DangerZone } from './delete-account'

// DangerZone ProfileInfo

// фичи для HeaderCreateQuiz
export { QuizHelp } from './quiz-help'
export { SaveQuiz } from './save-quiz'
// фичи для CreateQuizPage
export { QuizStats } from './quiz-editor'
export { QuizQuestions } from './quiz-editor'
// фичи для QuizSearch
export { QuizSearch } from './search-quiz'

export { loginSchema } from './auth'
export { registerSchema } from './auth'

export { LoginForm } from './auth'
export { RegistrationForm } from './auth'

// фичи для Quiz

export { QuizTimer } from './quiz-timer'
export { AnswerList } from './answer-selection'
export { QuizProgress } from './quiz-progress'
export { QuizActions } from './quiz-actions'
export { QuestionSection } from './question-section'
export { AnswerResult } from './answer-result'
export { calculatePartialScore } from './submit-answer'
export { checkAnswer } from './submit-answer'
export { useAnswerSelection } from './answer-selection'

// фичи для QuizFinish

export { getGrade } from './quiz-finish'
export { getMessage } from './quiz-finish'
export { getMotivation } from './quiz-finish'
// фичи для ProfileSettingsPage

export { ProfileInfo } from './edit-profile'

export { CreateTeamModal } from './create-team-modal'

// фичи для Quiz
export {
  AntiCheatProvider,
  useAntiCheatContext,
  WarningModal,
} from './anti-cheating'
export { RulesModal, RulesGate } from './rules'
// фичи для поиска
export { useAdminSearch, useQuizSearch } from './search-quiz'
