import React from 'react'

import { Input } from '@shared'

import styles from './Checkbox.module.scss'

export function Checkbox({ className, label, ...props }) {
  return (
    <label className={`${styles.checkboxLabel} ${className || ''}`}>
      <Input type="checkbox" {...props} />
      <span className={styles.checkboxCustom}></span>
      {label && <span className={styles.checkboxText}>{label}</span>}
    </label>
  )
}
