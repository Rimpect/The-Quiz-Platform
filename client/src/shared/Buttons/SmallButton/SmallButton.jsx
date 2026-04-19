import React from 'react'

export function SmallButton({ children, ...attributes }) {
  return (
    <button type="button" className="CustomSmallButton" {...attributes}>
      {children}
    </button>
  )
}
