import React, { useState } from 'react'

import { Input } from '@shared'
import { mediaService } from '@shared/api/services/mediaService'
import { Image } from 'lucide-react'
import { toast } from 'sonner'

import styles from './CoverUpload.module.scss'

export function CoverUpload({ value = '', onUpload }) {
  const [preview, setPreview] = useState('')
  const [loading, setLoading] = useState(false)

  const handleCoverUpload = async (e) => {
    const file = e.target.files[0]
    if (!file) return

    // Мгновенное локальное превью
    const reader = new FileReader()
    reader.onloadend = () => setPreview(reader.result)
    reader.readAsDataURL(file)

    // Загрузка на сервер -> webp -> URL
    setLoading(true)
    try {
      const res = await mediaService.uploadSimple('quiz', file)
      if (res?.url && onUpload) onUpload(res.url)
    } catch (err) {
      toast.error(err.message || 'Не удалось загрузить обложку')
      setPreview('')
    } finally {
      setLoading(false)
    }
  }

  const shownImage = preview || value

  return (
    <div className={styles.coverSection}>
      <div className={styles.coverLabel}>Обложка квиза</div>

      <Input
        type="file"
        id="coverInput"
        accept="image/png, image/jpeg, image/jpg, image/webp"
        onChange={handleCoverUpload}
        style={{ display: 'none' }}
      />

      <label htmlFor="coverInput" className={styles.coverButton}>
        {shownImage ? (
          <div className={styles.coverPreview}>
            <img src={shownImage} alt="Обложка квиза" />
            <div className={styles.coverOverlay}>
              <span>{loading ? 'Загрузка...' : 'Изменить обложку'}</span>
            </div>
          </div>
        ) : (
          <>
            <div className={styles.uploadIcon}>
              <Image size={50} color="gray"></Image>
            </div>
            <div className={styles.uploadText}>
              {loading ? 'Загрузка...' : 'Загрузить обложку'}
            </div>
            <div className={styles.uploadHint}>
              PNG, JPG до 5МБ. Рекомендуемый размер: 1200x630px
            </div>
          </>
        )}
      </label>
    </div>
  )
}
