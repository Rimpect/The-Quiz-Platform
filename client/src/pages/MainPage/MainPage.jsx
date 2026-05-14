import React from 'react'

import { QuizSearch, QuizeBoard } from '@widgets'

export function MainPage() {
  const currentPage = 1
  const totalPages = 7
  const onPageChange = 7

  return (
    <>
      <QuizSearch></QuizSearch>
      <QuizeBoard></QuizeBoard>
    </>
  )
}
