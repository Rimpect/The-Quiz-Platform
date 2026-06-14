import { Image, Video, Music } from 'lucide-react'

export const DIFFICULTY_OPTIONS = [
  { id: 'diff-all', label: 'Все', value: 'all' },
  { id: 'diff-easy', label: 'Лёгкий', value: 'easy' },
  { id: 'diff-medium', label: 'Средний', value: 'medium' },
  { id: 'diff-hard', label: 'Сложный', value: 'hard' },
]

export const TYPE_QUESTION_OPTIONS = [
  { id: 'tq-single', label: 'Одиночный выбор', value: 'single' },
  { id: 'tq-multiple', label: 'Множественный выбор', value: 'multiple' },
]

export const MEDIA_OPTIONS = [
  { id: 'media-image', label: 'Изображения', value: 'image', Icon: Image },
  { id: 'media-video', label: 'Видео', value: 'video', Icon: Video },
  { id: 'media-audio', label: 'Аудио', value: 'audio', Icon: Music },
]
