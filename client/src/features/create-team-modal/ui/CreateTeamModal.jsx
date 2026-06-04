import { useState } from 'react'

import { Button, Input } from '@shared'

import styles from './CreateTeamModal.module.scss'

export function CreateTeamModal({ isOpen, onClose, onCreate }) {
  const [teamName, setTeamName] = useState('')
  const [description, setDescription] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!teamName.trim()) return

    onCreate({
      name: teamName,
      description,
    })

    setTeamName('')
    setDescription('')
    onClose()
  }

  if (!isOpen) return null
  return (
    <div className={styles.overlay} onClick={onClose}>
      <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
        <h2 className={styles.title}>Создать команду</h2>

        <form className={styles.form} onSubmit={handleSubmit}>
          <Input
            type="text"
            placeholder="Название команды"
            value={teamName}
            onChange={(e) => setTeamName(e.target.value)}
          />

          <div className={styles.actions}>
            <Button variant="white" type="button" onClick={onClose}>
              Отмена
            </Button>
            <Button variant="black" type="submit">
              Создать
            </Button>
          </div>
        </form>
      </div>
    </div>
  )
}
