import React from 'react'

import styles from './Input.module.scss'

function Input({ className, type, ...props }) {
  return (
    <input
      type={type}
      data-slot="input"
      className={`${styles.input} ${className || ''}`}
      {...props}
    />
  )
}

export { Input }
