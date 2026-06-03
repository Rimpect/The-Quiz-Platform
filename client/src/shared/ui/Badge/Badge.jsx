import React from 'react'

import styles from './Badge.module.scss'

export function Badge({
  children,
  variant = 'default',
  size = 'md',
  className = '',
  ...props
}) {
  const variantClass = styles[`badge--${variant}`]
  const sizeClass = styles[`badge--${size}`]

  return (
    <span
      className={[styles.badge, variantClass, sizeClass, className]
        .filter(Boolean)
        .join(' ')}
      {...props}
    >
      {children}
    </span>
  )
}
