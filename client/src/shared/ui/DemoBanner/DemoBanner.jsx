import { useState } from 'react'

import { IS_DEMO, REPO_URL, ModalInfo } from '@shared'
import { Info, Github, Server } from 'lucide-react'

import styles from './DemoBanner.module.scss'

export function DemoBanner() {
  const [open, setOpen] = useState(false)

  if (!IS_DEMO) return null

  return (
    <>
      <div className={styles.banner}>
        <span className={styles.text}>Демо-версия со статичными данными.</span>
        <button
          type="button"
          className={styles.link}
          onClick={() => setOpen(true)}
        >
          О полной версии
        </button>
        <span className={styles.sep}>·</span>
        <a
          className={styles.link}
          href={REPO_URL}
          target="_blank"
          rel="noopener noreferrer"
        >
          GitHub
        </a>
      </div>

      {open && (
        <ModalInfo
          title="Полная версия"
          icon={<Server size={22} />}
          onClose={() => setOpen(false)}
        >
          <div className={styles.modalBody}>
            <p>
              Сейчас вы смотрите <b>демо-версию</b> со статичными данными: она
              работает полностью в браузере, без сервера.
            </p>
            <p>
              Полная версия — с регистрацией, командными и соревновательными
              квизами и мультиплеером в реальном времени — требует запущенного
              бэкенда. <b>Публичный хост пока не поднят</b>, поэтому
              онлайн-ссылки на неё временно нет.
            </p>
            <p className={styles.modalHint}>
              <Info size={16} />
              Развернуть полную версию можно локально по инструкции в
              репозитории (<code>docker compose up</code>).
            </p>
            <a
              className={styles.modalRepoLink}
              href={REPO_URL}
              target="_blank"
              rel="noopener noreferrer"
            >
              <Github size={18} />
              Открыть репозиторий на GitHub
            </a>
          </div>
        </ModalInfo>
      )}
    </>
  )
}
