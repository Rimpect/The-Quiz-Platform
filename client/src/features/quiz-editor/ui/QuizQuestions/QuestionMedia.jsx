import React, { useRef, useState } from 'react'

import { Button } from '@shared'
import { mediaService } from '@shared/api/services/mediaService'
import { Image, Video, Music, X } from 'lucide-react'
import { toast } from 'sonner'

import styles from './QuizQuestion.module.scss'

const TARGETS = {
  image: { target: 'question_image', accept: 'image/*' },
  video: { target: 'question_video', accept: 'video/*' },
  audio: { target: 'question_audio', accept: 'audio/*' },
}

const isImageUrl = (url) => /\.(webp|png|jpe?g|gif|bmp|tiff)$/i.test(url || '')

export function QuestionMedia({ mediaUrl, onUpload }) {
  const [loading, setLoading] = useState(false)
  const inputRef = useRef(null)
  const kindRef = useRef('image')

  const pick = (kind) => {
    kindRef.current = kind
    if (inputRef.current) {
      inputRef.current.accept = TARGETS[kind].accept
      inputRef.current.value = ''
      inputRef.current.click()
    }
  }

  const handleFile = async (e) => {
    const file = e.target.files[0]
    if (!file) return
    setLoading(true)
    try {
      const res = await mediaService.uploadSimple(
        TARGETS[kindRef.current].target,
        file,
      )
      if (res?.url) onUpload(res.url)
    } catch (err) {
      toast.error(err.message || 'Не удалось загрузить медиа')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className={styles.mediaSection}>
      <div className={styles.fieldLabel}>Добавить медиа</div>

      <div className={styles.mediaButtons}>
        <Button
          variant="white"
          size="medium"
          type="button"
          icon={<Image size={20} />}
          onClick={() => pick('image')}
          disabled={loading}
        >
          картинка
        </Button>

        <Button
          variant="white"
          size="medium"
          type="button"
          icon={<Video size={20} />}
          onClick={() => pick('video')}
          disabled={loading}
        >
          Видео
        </Button>

        <Button
          variant="white"
          size="medium"
          type="button"
          icon={<Music size={20} />}
          onClick={() => pick('audio')}
          disabled={loading}
        >
          Аудио
        </Button>
      </div>

      <input
        ref={inputRef}
        type="file"
        onChange={handleFile}
        style={{ display: 'none' }}
      />

      {loading && <div className={styles.mediaHint}>Загрузка...</div>}

      {mediaUrl && !loading && (
        <div className={styles.mediaPreview}>
          {isImageUrl(mediaUrl) ? (
            <img src={mediaUrl} alt="Медиа вопроса" />
          ) : (
            <span>Медиа прикреплено</span>
          )}
          <Button
            variant="transparent"
            size="medium"
            type="button"
            icon={<X size={18} color="red" />}
            onClick={() => onUpload('')}
          />
        </div>
      )}
    </div>
  )
}
