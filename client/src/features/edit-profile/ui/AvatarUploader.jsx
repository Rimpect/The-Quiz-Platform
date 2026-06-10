import React, { useState, useRef } from 'react'

import { Button, Input } from '@shared'

import styles from './AvatarUploader.module.scss'

export function AvatarUploader({ onAvatarChange, initialAvatar = null }) {
  const [avatar, setAvatar] = useState(initialAvatar)
  const [error, setError] = useState('')
  const fileInputRef = useRef(null)

  const MAX_FILE_SIZE = 2 * 1024 * 1024 // 2MB
  const ALLOWED_TYPES = ['image/jpeg', 'image/jpg', 'image/png']

  const handleFileSelect = () => {
    fileInputRef.current.click()
  }

  const handleFileChange = (event) => {
    const file = event.target.files[0]

    if (!file) return

    if (!ALLOWED_TYPES.includes(file.type)) {
      setError('Можно загружать только JPG, JPEG или PNG файлы')
      console.error('Ошибка: неподдерживаемый тип файла', file.type)
      return
    }

    // Валидация размера файла
    if (file.size > MAX_FILE_SIZE) {
      setError('Размер файла не должен превышать 2МБ')
      console.error(
        'Ошибка: файл слишком большой',
        `${(file.size / 1024 / 1024).toFixed(2)}MB`,
      )
      return
    }

    setError('')

    // Вывод в консоль информации о загрузке
    console.log('Файл успешно загружен:', {
      name: file.name,
      type: file.type,
      size: `${(file.size / 1024).toFixed(2)} KB`,
      lastModified: new Date(file.lastModified).toLocaleString(),
    })

    // Создание превью
    const reader = new FileReader()
    reader.onloadend = () => {
      const avatarData = reader.result
      setAvatar(avatarData)
      console.log('Аватар успешно установлен')

      // Если передан колбэк, вызываем его с данными аватара
      if (onAvatarChange) {
        onAvatarChange(avatarData, file)
      }
    }
    reader.readAsDataURL(file)
  }

  return (
    <div>
      <div className={styles.avatarBlock}>
        {avatar ? (
          <img src={avatar} alt="avatar" className={styles.avatar} />
        ) : (
          <div className={styles.avatar}></div>
        )}
        <div className={styles.buttonBlock}>
          <Input
            ref={fileInputRef}
            type="file"
            accept="image/jpeg,image/jpg,image/png"
            onChange={handleFileChange}
            style={{ display: 'none' }}
          />
          <Button variant="white" onClick={handleFileSelect}>
            Загрузить фото
          </Button>
          <span className={styles.sizePhoto}>JPG, PNG. Максимум 2МБ</span>
          {error && <span className={styles.error}>{error}</span>}
        </div>
      </div>
    </div>
  )
}
