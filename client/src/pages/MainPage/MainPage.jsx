import React from 'react'

import { QuizSearch } from '../../widgets/QuizSearch/QuizSearch'

import { QuizeBoard } from './../../widgets/QuizeBoard/QuizeBoard'

export function MainPage() {
  return (
    <>
      {/* <UserAction></UserAction> */}
      <QuizSearch></QuizSearch>
      <QuizeBoard></QuizeBoard>
    </>
  )
}
