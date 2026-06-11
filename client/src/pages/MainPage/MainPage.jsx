import React, { useState } from 'react'

import { QuizToolbar, QuizBoard } from '@widgets'

export function MainPage() {
  const [currentPage, setCurrentPage] = useState(1)

  return (
    <>
      <QuizToolbar />
      <QuizBoard currentPage={currentPage} onPageChange={setCurrentPage} />
    </>
  )
}
