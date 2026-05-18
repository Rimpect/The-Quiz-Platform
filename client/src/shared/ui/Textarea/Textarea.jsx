import React from 'react'

import styles from './Textarea.module.scss'

function Textarea({ className, ...props }) {
  return (
    <textarea
      data-slot="textarea"
      className={`${styles.textarea} ${className || ''}`}
      {...props}
    />
  )
}

export { Textarea }
