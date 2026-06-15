import React from 'react'

import styles from './Radio.module.scss'

function Radio({ className, label, ...props }) {
  return (
    <label className={`${styles.radioLabel} ${className || ''}`}>
      <input type="radio" {...props} />
      <span className={styles.radioCustom}></span>
      {label && <span className={styles.radioText}>{label}</span>}
    </label>
  )
}

export { Radio }
