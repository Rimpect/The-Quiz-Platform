import React from 'react'
import './AverageButton.scss'

export function AverageButton({ children, ...attributes }) {
  return (
    <button type="button" className="CustomAverageButton" {...attributes}>
      {children}
    </button>
  )
}
