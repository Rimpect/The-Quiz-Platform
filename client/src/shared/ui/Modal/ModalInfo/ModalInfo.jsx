import { useEffect } from 'react'

import { X } from 'lucide-react'

import styles from './ModalInfo.module.scss'

/**
 * Универсальная информационная модалка (правила, FAQ и т.п.) без принятия.
 * Закрывается по клику на оверлей, кнопке и Esc; скролл фона блокируется.
 */
export function ModalInfo({ title, icon, onClose, children }) {
  useEffect(() => {
    document.body.style.overflow = 'hidden'
    const handleEsc = (e) => {
      if (e.key === 'Escape') onClose()
    }
    window.addEventListener('keydown', handleEsc)
    return () => {
      document.body.style.overflow = 'unset'
      window.removeEventListener('keydown', handleEsc)
    }
  }, [onClose])

  return (
    <div className={styles.overlay} onClick={onClose}>
      <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
        <button className={styles.closeBtn} onClick={onClose}>
          <X size={24} />
        </button>

        <div className={styles.header}>
          {icon && <span className={styles.headerIcon}>{icon}</span>}
          <h2 className={styles.title}>{title}</h2>
        </div>

        <div className={styles.content}>{children}</div>
      </div>
    </div>
  )
}
