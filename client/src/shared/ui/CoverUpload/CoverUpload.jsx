import React, { useState } from 'react'

import { Input } from '@shared'
import { Image } from 'lucide-react'

import styles from './CoverUpload.module.scss'

export function CoverUpload() {
  const [coverImage, setCoverImage] = useState(null)

  const handleCoverUpload = (e) => {
    const file = e.target.files[0]
    if (file) {
      const reader = new FileReader()
      reader.onloadend = () => {
        setCoverImage(reader.result)
      }
      reader.readAsDataURL(file)
    }
  }

  return (
    <div className={styles.coverSection}>
      <div className={styles.coverLabel}>Обложка квиза</div>

      <Input
        type="file"
        id="coverInput"
        accept="image/png, image/jpeg, image/jpg"
        onChange={handleCoverUpload}
        style={{ display: 'none' }}
      />

      <label htmlFor="coverInput" className={styles.coverButton}>
        {coverImage ? (
          <div className={styles.coverPreview}>
            <img src={coverImage} alt="Обложка квиза" />
            <div className={styles.coverOverlay}>
              <span>Изменить обложку</span>
            </div>
          </div>
        ) : (
          <>
            <div className={styles.uploadIcon}>
              <Image size={50} color="gray"></Image>
            </div>
            <div className={styles.uploadText}>Загрузить обложку</div>
            <div className={styles.uploadHint}>
              PNG, JPG до 5МБ. Рекомендуемый размер: 1200x630px
            </div>
          </>
        )}
      </label>
    </div>
  )
}
