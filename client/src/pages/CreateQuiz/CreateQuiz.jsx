import React from 'react'

import { ProfileStats } from '../../widgets/ProfileStats/ProfileStats'
import { QuizHistory } from '../../widgets/QuizHistory/QuizHistory'

export default function CreateQuiz() {
  return (
    <>
      <ProfileStats></ProfileStats>
      <QuizHistory></QuizHistory>
    </>
  )
}
