import {
  AnswerSection,
  SubmitAnswerButton,
  NextQuestionButton,
  SkipQuestionButton,
  QuizProgress,
  QuizTimer,
  LeaderboardPreview,
} from '@features'

import { QuestionCard } from '@entities'

import { useQuizPlayer } from '../model/useQuizPlayer'

export function QuizPlayer() {
  const {
    currentQ,
    progress,
    isAnswered,
    selectedAnswers,

    handleSelectAnswer,
    handleSubmitAnswer,
    handleNextQuestion,
    handleSkipQuestion,
  } = useQuizPlayer()

  return (
    <>
      <QuizProgress progress={progress} />

      <QuizTimer />

      <QuestionCard question={currentQ} />

      <AnswerSection
        question={currentQ}
        selectedAnswers={selectedAnswers}
        isAnswered={isAnswered}
        onSelect={handleSelectAnswer}
      />

      {!isAnswered ? (
        <SubmitAnswerButton onClick={handleSubmitAnswer} />
      ) : (
        <NextQuestionButton onClick={handleNextQuestion} />
      )}

      <SkipQuestionButton onClick={handleSkipQuestion} />

      <LeaderboardPreview />
    </>
  )
}
