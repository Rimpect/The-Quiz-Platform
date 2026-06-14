import { useEffect, useRef } from 'react'

const TICTAK = '/The-Quiz-Platform/sounds/tictak.mp3'
const BELL = '/The-Quiz-Platform/sounds/bell-sound.mp3'

/**
 * Звук таймера, завязанный на ВНЕШНЕЕ (серверное) время.
 * Поведение одинаково для квизов и лобби: «тиканье» за `threshold` секунд до
 * конца + «звонок» в момент окончания. Используется там, где отсчёт идёт с
 * сервера и нет локального useTimer (synced-квизы и лобби).
 *
 * @param {number|null} timeLeft — оставшееся время в секундах (с сервера)
 * @param {object}  opts
 * @param {number}  opts.threshold — за сколько секунд до конца начинать тиканье
 * @param {boolean} opts.enabled
 */
export function useTimerSound(
  timeLeft,
  { threshold = 10, enabled = true } = {},
) {
  const warnRef = useRef(null) // tictak.mp3 (управляемый — можно остановить)
  const prevRef = useRef(null)
  const warnedRef = useRef(false) // «тик» уже сыгран на этом отсчёте
  const endedRef = useRef(false) // «звонок» уже сыгран

  // Инициализация аудио + разблокировка autoplay по первому жесту пользователя
  useEffect(() => {
    if (!enabled) return undefined

    const warn = new Audio(TICTAK)
    warnRef.current = warn

    const unlock = () => {
      warn
        .play()
        .then(() => {
          warn.pause()
          warn.currentTime = 0
        })
        .catch(() => {})
      window.removeEventListener('pointerdown', unlock)
      window.removeEventListener('keydown', unlock)
    }
    window.addEventListener('pointerdown', unlock)
    window.addEventListener('keydown', unlock)

    return () => {
      window.removeEventListener('pointerdown', unlock)
      window.removeEventListener('keydown', unlock)
      warn.pause()
    }
  }, [enabled])

  useEffect(() => {
    if (!enabled || timeLeft == null) return
    const warn = warnRef.current
    if (!warn) return

    const prev = prevRef.current
    prevRef.current = timeLeft

    // Время выросло → начался новый отсчёт (следующий вопрос) → сброс флагов
    if (prev != null && timeLeft > prev) {
      warnedRef.current = false
      endedRef.current = false
      warn.pause()
      warn.currentTime = 0
    }

    // Конец времени → «звонок»
    if (timeLeft <= 0) {
      if (!endedRef.current) {
        endedRef.current = true
        warn.pause()
        warn.currentTime = 0
        // fire-and-forget: звонок доиграет, даже если экран сменится (лобби→квиз)
        new Audio(BELL).play().catch(() => {})
      }
      return
    }

    // Вход в зону предупреждения → одно проигрывание «тиканья»
    if (timeLeft <= threshold && !warnedRef.current) {
      warnedRef.current = true
      warn.currentTime = 0
      warn.play().catch(() => {})
    }
  }, [timeLeft, threshold, enabled])
}
