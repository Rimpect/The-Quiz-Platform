import { useState } from 'react'

import { Button, ROUTES, Input } from '@shared'
import { Clock, Users } from 'lucide-react'
import { Link } from 'react-router-dom'

import styles from '../LobbyTeams.module.scss'

const WAIT_PRESETS = [15, 30, 60, 120, 300]

export function PreLobby({ quiz, loading, onCreate, onJoinByCode }) {
  const [waitSeconds, setWaitSeconds] = useState(30)
  const [codeInput, setCodeInput] = useState('')

  return (
    <div className={styles.preLobby}>
      <div className={styles.preCard}>
        <Users size={40} className={styles.preIcon} />
        <h1>{quiz.title}</h1>
        <p className={styles.preHint}>Командный режим</p>

        <div className={styles.waitSetting}>
          <span className={styles.waitLabel}>
            <Clock size={16} /> Время ожидания игроков
          </span>
          <div className={styles.waitPresets}>
            {WAIT_PRESETS.map((sec) => (
              <button
                key={sec}
                type="button"
                className={`${styles.waitPreset} ${
                  waitSeconds === sec ? styles.waitPresetActive : ''
                }`}
                onClick={() => setWaitSeconds(sec)}
              >
                {sec < 60 ? `${sec} сек` : `${sec / 60} мин`}
              </button>
            ))}
          </div>
        </div>

        <Button
          variant="black"
          fullWidth
          onClick={() => onCreate(waitSeconds)}
          disabled={loading}
        >
          Создать лобби
        </Button>

        <div className={styles.preDivider}>или войдите по коду</div>

        <div className={styles.codeRow}>
          <Input
            type="text"
            placeholder="Код приглашения"
            value={codeInput}
            maxLength={6}
            onChange={(e) => setCodeInput(e.target.value.toUpperCase())}
          />
          <Button
            variant="green"
            onClick={() => onJoinByCode(codeInput)}
            disabled={loading || codeInput.trim().length < 4}
          >
            Войти
          </Button>
        </div>

        <Link to={ROUTES.main} className={styles.preBack}>
          Назад
        </Link>
      </div>
    </div>
  )
}
