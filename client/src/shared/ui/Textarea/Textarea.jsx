import React from 'react'

import styles from './Textarea.module.scss'

function Textarea({ className, maxLength, ...props }) {
  const computedMaxLength = maxLength ?? 500

  return (
    <textarea
      data-slot="textarea"
      className={`${styles.textarea} ${className || ''}`}
      maxLength={computedMaxLength}
      {...props}
    />
  )
}

export { Textarea }
