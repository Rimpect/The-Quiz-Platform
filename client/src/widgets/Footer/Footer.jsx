import { useState } from 'react'

import { ModalInfo } from '@shared'
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

      {openModal === 'help' && (
        <ModalInfo
          title="Как пользоваться QuizMaster"
          icon="🧭"
          onClose={close}
        >
          <div className={styles.guide}>
            <section>
              <h4>🔎 Поиск и запуск квиза</h4>
              <p>
                На главной выберите квиз через поиск или фильтры (категория,
                сложность, тип). Откройте карточку и нажмите «Играть» —
                выбранный режим запустит прохождение.
              </p>
            </section>

            <section>
              <h4>🎮 Режимы игры</h4>
              <ul>
                <li>
                  <strong>Одиночный</strong> — проходите квиз сами в своём
                  темпе.
                </li>
                <li>
                  <strong>Рейтинговый</strong> — результат идёт в общий
                  лидерборд квиза.
                </li>
                <li>
                  <strong>Командный</strong> — игра командами по коду лобби:
                  капитан фиксирует ответ, остальные голосуют.
                </li>
              </ul>
              <p className={styles.note}>
                🔒 Рейтинговый и командный режимы доступны только после входа в
                аккаунт. Без авторизации можно играть квизы в одиночном режиме.
              </p>
            </section>

            <section>
              <h4>🏆 Баллы и лидерборд</h4>
              <p>
                За каждый вопрос начисляются баллы (во множественном выборе —
                пропорционально верным ответам). Итог попадает в таблицу
                результатов и общий рейтинг квиза.
              </p>
            </section>

            <section>
              <h4>👤 Профиль</h4>
              <p>
                В личном кабинете видны ваши созданные квизы, история
                прохождений, достижения и статистика. Там же можно редактировать
                профиль.
              </p>
            </section>

            <section>
              <h4>🛡️ Честная игра</h4>
              <p>
                Во время прохождения действует защита от списывания. Подробности
                — в разделе «Правила» внизу страницы.
              </p>
            </section>
          </div>
        </ModalInfo>
      )}

      {openModal === 'rules' && (
        <ModalInfo title="Правила прохождения квиза" icon="🎯" onClose={close}>
          <p>
            Для честной игры во время прохождения квиза действуют следующие
            правила:
          </p>
          <ul className={styles.modalList}>
            <li>
              <strong>🚫 Не переключайте вкладки.</strong> Переключение на
              другую вкладку фиксируется как нарушение.
            </li>
            <li>
              <strong>📋 Копирование и вставка запрещены.</strong> Скопировать
              или вставить текст не получится.
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
      )}

      {openModal === 'faq' && (
        <ModalInfo title="Часто задаваемые вопросы" icon="❓" onClose={close}>
          <ul className={styles.faqList}>
            <li>
              <strong>Как создать свой квиз?</strong>
              <p>
                Войдите в аккаунт, откройте «Создать квиз», заполните название,
                описание, обложку и вопросы. После отправки квиз попадёт на
                модерацию.
              </p>
            </li>
            <li>
              <strong>Чем отличаются режимы игры?</strong>
              <p>
                Одиночный — проходите сами; рейтинговый — результат идёт в общий
                лидерборд; командный — играете командами, ответ за команду даёт
                капитан.
              </p>
            </li>
            <li>
              <strong>Как работает командный режим?</strong>
              <p>
                Хост создаёт лобби с кодом приглашения и таймером ожидания.
                Участники делятся на команды; капитан фиксирует ответ, остальные
                голосуют. Переход к следующему вопросу — когда ответили все
                капитаны или вышло время.
              </p>
            </li>
            <li>
              <strong>Нужна ли регистрация, чтобы играть?</strong>
              <p>
                Одиночные квизы доступны без входа. Рейтинговый и командный
                режимы — только после авторизации: для рейтинга результат
                сохраняется в общий лидерборд, а в командном нужен ваш профиль и
                аватар в лобби.
              </p>
            </li>
            <li>
              <strong>Почему меня заблокировало в квизе?</strong>
              <p>
                Сработала защита от списывания (3 нарушения). Подробности — в
                разделе «Правила».
              </p>
            </li>
          </ul>
        </ModalInfo>
      )}
    </footer>
  )
}
