import clsx from 'clsx'

import styles from './Button.module.scss'

export function Button({
  variant = 'primary',
  size = 'medium',
  icon,
  iconPosition = 'left',
  children,
  fullWidth = false,
  disabled = false,
  active = false, // Добавить
  className,
  ...props
}) {
  return (
    <button
      className={clsx(
        styles.button,
        styles[variant],
        styles[size],
        {
          [styles.fullWidth]: fullWidth,
          [styles.disabled]: disabled,
          [styles.active]: active,
        },
        className,
      )}
      disabled={disabled}
      {...props}
    >
      {icon && iconPosition === 'left' && (
        <span className={styles.icon}>{icon}</span>
      )}

      {children && <span>{children}</span>}

      {icon && iconPosition === 'right' && (
        <span className={styles.icon}>{icon}</span>
      )}
    </button>
  )
}
