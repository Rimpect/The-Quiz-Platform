import styles from './Input.module.scss'

function Input({ className, type, maxLength, ...props }) {
  const computedMaxLength =
    maxLength ??
    (type === 'text' ||
    type === 'search' ||
    type === 'email' ||
    type === 'tel' ||
    type === 'url'
      ? 100
      : type === 'password'
        ? 64
        : undefined)

  return (
    <input
      type={type}
      data-slot="input"
      maxLength={computedMaxLength}
      className={`${styles.input} ${className || ''}`}
      {...props}
    />
  )
}

export { Input }
