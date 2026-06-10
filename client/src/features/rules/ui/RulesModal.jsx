import React, { useState } from 'react'

import { Input } from '@shared'

import styles from './RulesModal.module.scss'

export const RulesModal = ({ isOpen, onAccept, onDecline }) => {
  const [isChecked, setIsChecked] = useState(false)

  if (!isOpen) return null

  return (
    <div className={styles.overlay}>
      <div className={styles.modal}>
        <div className={styles.header}>
          <span className={styles.icon}>🎯</span>
          <h2>Правила прохождения квиза</h2>
        </div>

        <div className={styles.content}>
          <p>
            Для обеспечения честной игры, пожалуйста, ознакомьтесь с правилами:
          </p>

          <ul className={styles.rulesList}>
            <li>
              <span className={styles.ruleIcon}>🚫</span>
              <div>
                <strong>Не переключайте вкладки</strong>
                <p>
                  Переключение на другую вкладку будет зафиксировано как
                  нарушение
                </p>
              </div>
            </li>

            <li>
              <span className={styles.ruleIcon}>📋</span>
              <div>
                <strong>Копирование и вставка запрещены</strong>
                <p>Вы не сможете скопировать или вставить текст</p>
              </div>
            </li>

            <li>
              <span className={styles.ruleIcon}>🔧</span>
              <div>
                <strong>Инструменты разработчика отключены</strong>
                <p>Открытие DevTools (F12) будет зафиксировано как нарушение</p>
              </div>
            </li>

            <li>
              <span className={styles.ruleIcon}>⚠️</span>
              <div>
                <strong>3 нарушения = блокировка</strong>
                <p>После 3 нарушений квиз автоматически завершится</p>
              </div>
            </li>
          </ul>

          <div className={styles.checkboxWrapper}>
            <label className={styles.checkbox}>
              <Input
                type="checkbox"
                checked={isChecked}
                onChange={(e) => setIsChecked(e.target.checked)}
              />
              <span>Я ознакомлен(а) и согласен(на) с правилами</span>
            </label>
          </div>
        </div>

        <div className={styles.footer}>
          <button className={styles.declineButton} onClick={onDecline}>
            Отказаться
          </button>
          <button
            className={styles.acceptButton}
            onClick={onAccept}
            disabled={!isChecked}
          >
            Начать квиз
          </button>
        </div>
      </div>
    </div>
  )
}
