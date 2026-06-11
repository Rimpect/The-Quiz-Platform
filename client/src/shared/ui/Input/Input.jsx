import styles from './Input.module.scss'

function Input({ className, type, maxLength, variant = 'default', ...props }) {
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

  const getVariantClass = () => {
    switch (variant) {
      case 'search':
        return styles.search
      case 'error':
        return styles.error
      case 'success':
        return styles.success
      case 'filled':
        return styles.filled
      case 'form':
        return styles.form
      default:
        return styles.default
    }
  }

  return (
    <input
      type={type}
      data-slot="input"
      maxLength={computedMaxLength}
      className={`${styles.input} ${getVariantClass()} ${className || ''}`}
      {...props}
    />
  )
}

export { Input }
