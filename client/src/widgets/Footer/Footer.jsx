import { useState } from 'react'

import { HelpModal, RulesInfoModal, FaqModal } from '@features'
import { Mail, Phone, MapPin } from 'lucide-react'

import styles from './Footer.module.scss'

export function Footer() {
  const [openModal, setOpenModal] = useState(null) // 'help' | 'rules' | 'faq' | null
  const close = () => setOpenModal(null)

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
            <li>
              <button
                type="button"
                className={styles.linkButton}
                onClick={() => setOpenModal('help')}
              >
                Помощь
              </button>
            </li>
            <li>
              <button
                type="button"
                className={styles.linkButton}
                onClick={() => setOpenModal('faq')}
              >
                FAQ
              </button>
            </li>
            <li>
              <button
                type="button"
                className={styles.linkButton}
                onClick={() => setOpenModal('rules')}
              >
                Правила
              </button>
            </li>
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

      {openModal === 'help' && <HelpModal onClose={close} />}
      {openModal === 'rules' && <RulesInfoModal onClose={close} />}
      {openModal === 'faq' && <FaqModal onClose={close} />}
    </footer>
  )
}
