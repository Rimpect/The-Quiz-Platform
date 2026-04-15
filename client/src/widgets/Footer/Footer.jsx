import React from 'react'

import { Mail, Phone, MapPin } from 'lucide-react'

import styles from './Footer.module.scss'

export function Footer() {
  return (
    <footer className={styles.footerContainer}>
      <div className={styles.footerInner}>
        <div className={styles.description}>
          <p className={styles.descriptionHeader}>О QuizMaster</p>
          <p className={styles.descriptionTitle}>
            Платформа для проведения <br />
            интеллектуальных квизов. Проверьте свои <br />
            знания и соревнуйтесь с друзьями!
          </p>
        </div>

        <div className={styles.menu}>
          <ul className={styles.list}>
            <li className={styles.listItem}>Поддержка</li>
            <li className={styles.listItem}>Помощь</li>
            <li className={styles.listItem}>FAQ</li>
            <li className={styles.listItem}>Правила</li>
          </ul>

          <ul className={styles.list}>
            <li className={styles.listItem}>Контакты</li>
            <li className={styles.listItem}>
              <Mail className={styles.listIcon} />
              info@quizmaster.ru
            </li>
            <li className={styles.listItem}>
              <Phone className={styles.listIcon} />
              +7 (495) 123-45-67
            </li>
            <li className={styles.listItem}>
              <MapPin className={styles.listIcon} />
              Россия
            </li>
          </ul>
        </div>
      </div>

      <div className={styles.copyright}>
        <p>&copy; 2026 QuizMaster. Все права защищены.</p>
      </div>
    </footer>
  )
}
