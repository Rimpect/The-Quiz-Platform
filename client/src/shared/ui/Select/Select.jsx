import React from 'react'

import styles from './Select.module.scss'

function Select({ className, children, ...props }) {
  return (
    <select
      data-slot="select"
      className={`${styles.select} ${className || ''}`}
      {...props}
    >
      {children}
    </select>
  )
}

export { Select }
