import { useState } from 'react'

import { ArrowLeft, Camera, Save } from 'lucide-react'

import styles from './ProfileSettings.module.scss'

export function ProfileSettings({ user = {}, onBack, onSave }) {
  const [name, setName] = useState(user.name || '')
  const [email, setEmail] = useState(user.email || '')
  const [currentPassword, setCurrentPassword] = useState('')
  const [newPassword, setNewPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [error, setError] = useState('')

  const handleSaveProfile = () => {
    if (!name.trim()) {
      setError('Введите имя')
      return
    }

    if (!email.trim()) {
      setError('Введите email')
      return
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(email)) {
      setError('Введите корректный email')
      return
    }

    setError('')
    onSave({ ...user, name, email })
  }

  const handleChangePassword = () => {
    if (!currentPassword.trim()) {
      setError('Введите текущий пароль')
      return
    }

    if (!newPassword.trim()) {
      setError('Введите новый пароль')
      return
    }

    if (newPassword.length < 6) {
      setError('Пароль должен содержать минимум 6 символов')
      return
    }

    if (newPassword !== confirmPassword) {
      setError('Пароли не совпадают')
      return
    }

    setError('')
    setCurrentPassword('')
    setNewPassword('')
    setConfirmPassword('')
  }

  return (
    <div className={styles.container}>
      <div className={styles.contentWrapper}>
        <button className={styles.backButton} onClick={onBack}>
          <ArrowLeft className={styles.backIcon} />
          Назад в личный кабинет
        </button>

        <h1 className={styles.title}>Настройки профиля</h1>

        {error && <div className={styles.errorMessage}>{error}</div>}

        <div className={styles.sections}>
          {/* Фото профиля */}
          <div className={styles.card}>
            <h2 className={styles.cardTitle}>Фото профиля</h2>
            <div className={styles.avatarSection}>
              <div className={styles.avatar}>
                {user.avatar ? (
                  <img
                    src={user.avatar}
                    alt={name}
                    className={styles.avatarImage}
                  />
                ) : (
                  <div className={styles.avatarFallback}>
                    {name.charAt(0) || '?'}
                  </div>
                )}
              </div>
              <div>
                <button className={styles.uploadButton}>
                  <Camera className={styles.buttonIcon} />
                  Загрузить фото
                </button>
                <p className={styles.uploadHint}>JPG, PNG. Максимум 2МБ</p>
              </div>
            </div>
          </div>

          {/* Личная информация */}
          <div className={styles.card}>
            <h2 className={styles.cardTitle}>Личная информация</h2>
            <div className={styles.formGroup}>
              <div className={styles.field}>
                <label htmlFor="name" className={styles.label}>
                  Имя
                </label>
                <input
                  id="name"
                  type="text"
                  className={styles.input}
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                />
              </div>

              <div className={styles.field}>
                <label htmlFor="email" className={styles.label}>
                  Email
                </label>
                <input
                  id="email"
                  type="email"
                  className={styles.input}
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              </div>

              <button className={styles.saveButton} onClick={handleSaveProfile}>
                <Save className={styles.buttonIcon} />
                Сохранить изменения
              </button>
            </div>
          </div>

          {/* Изменение пароля */}
          <div className={styles.card}>
            <h2 className={styles.cardTitle}>Изменить пароль</h2>
            <div className={styles.formGroup}>
              <div className={styles.field}>
                <label htmlFor="currentPassword" className={styles.label}>
                  Текущий пароль
                </label>
                <input
                  id="currentPassword"
                  type="password"
                  className={styles.input}
                  placeholder="••••••••"
                  value={currentPassword}
                  onChange={(e) => setCurrentPassword(e.target.value)}
                />
              </div>

              <div className={styles.field}>
                <label htmlFor="newPassword" className={styles.label}>
                  Новый пароль
                </label>
                <input
                  id="newPassword"
                  type="password"
                  className={styles.input}
                  placeholder="••••••••"
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                />
              </div>

              <div className={styles.field}>
                <label htmlFor="confirmNewPassword" className={styles.label}>
                  Подтвердите новый пароль
                </label>
                <input
                  id="confirmNewPassword"
                  type="password"
                  className={styles.input}
                  placeholder="••••••••"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                />
              </div>

              <button
                className={styles.passwordButton}
                onClick={handleChangePassword}
              >
                Изменить пароль
              </button>
            </div>
          </div>

          {/* Опасная зона */}
          <div className={`${styles.card} ${styles.dangerCard}`}>
            <h2 className={styles.dangerTitle}>Опасная зона</h2>
            <p className={styles.dangerText}>
              После удаления аккаунта все ваши данные будут безвозвратно
              потеряны.
            </p>
            <button className={styles.deleteButton}>Удалить аккаунт</button>
          </div>
        </div>
      </div>
    </div>
  )
}
