import React from 'react'
import './QuizButton.scss'

export function QuizButton({ children, ...attributes }) {
  return (
    <button type="button" className="CustomQuizButton" {...attributes}>
      {children}
    </button>
  )
}
