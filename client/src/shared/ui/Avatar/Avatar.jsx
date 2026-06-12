import { User } from 'lucide-react'

import styles from './Avatar.module.scss'

/**
 * Аватар пользователя. По умолчанию — синий кружок с иконкой,
 * если есть src — показывает фото. Используется везде (шапка, лобби, профиль).
 */
export function Avatar({ src, alt = '', size = 36 }) {
  return (
    <div className={styles.avatar} style={{ width: size, height: size }}>
      {src ? (
        <img src={src} alt={alt} className={styles.img} />
      ) : (
        <User size={Math.round(size * 0.55)} className={styles.icon} />
      )}
    </div>
  )
}
