import { ModalInfo } from '@shared'

import styles from './InfoModals.module.scss'

export function RulesInfoModal({ onClose }) {
  return (
    <ModalInfo title="Правила прохождения квиза" icon="🎯" onClose={onClose}>
      <p>
        Для честной игры во время прохождения квиза действуют следующие правила:
      </p>
      <ul className={styles.modalList}>
        <li>
          <strong>🚫 Не переключайте вкладки.</strong> Переключение на другую
          вкладку фиксируется как нарушение.
        </li>
        <li>
          <strong>📋 Копирование и вставка запрещены.</strong> Скопировать или
          вставить текст не получится.
        </li>
        <li>
          <strong>🔧 Инструменты разработчика отключены.</strong> Открытие
          DevTools (F12) фиксируется как нарушение.
        </li>
        <li>
          <strong>⚠️ 3 нарушения — блокировка.</strong> После трёх нарушений
          квиз автоматически завершится.
        </li>
        <li>
          <strong>👑 Командный режим.</strong> Решение принимает капитан
          команды; остальные участники голосуют за варианты.
        </li>
      </ul>
    </ModalInfo>
  )
}
