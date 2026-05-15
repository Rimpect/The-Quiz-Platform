import { useState } from 'react'

import { Button } from '@shared'
import { Save } from 'lucide-react'
import styles from './ProfileInfo.module.scss'

export function ProfileInfo({ user }) {
  const [name, setName] = useState(user.name)

  const [email, setEmail] = useState(user.email)

  const handleSave = () => {
    // TODO: api request

    console.log({
      name,
      email,
    })

    alert('Профиль обновлен')
  }

  return (
    <div className={styles.card}>
      <h2 className={styles.title}>Личная информация</h2>

      <div className={styles.avatarBlock}>
        {/* <img src={user.avatar} alt="avatar" className={styles.avatar} /> */}
        <div className={styles.avatar}></div>
        <div className={styles.buttonBlock}>
          <Button variant="white">Загрузить фото</Button>
          <span span className={styles.sizePhoto}>
            JPG, PNG. Максимум 2МБ
          </span>
        </div>
      </div>

      <div className={styles.field}>
        <label>Имя</label>

        <input value={name} onChange={(e) => setName(e.target.value)} />
      </div>

      <div className={styles.field}>
        <label>Email</label>

        <input value={email} onChange={(e) => setEmail(e.target.value)} />
      </div>

      <Button variant="white" icon={<Save />} onClick={handleSave}>
        Сохранить изменения
      </Button>
    </div>
  )
}
