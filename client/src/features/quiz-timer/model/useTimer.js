import { useEffect, useRef, useState } from 'react'

const WARNING_TIME = 10

export function useTimer({
  duration,
  onTimeEnd,
  enableSound = true,
  isLobby = false,
  lobbyWarningThreshold = 5,
}) {
  const [timeLeft, setTimeLeft] = useState(duration)

  const hasEnded = useRef(false)
  const hasPlayedWarning = useRef(false)
  const warningTimeoutRef = useRef(null)

  const warningSoundRef = useRef(null)
  const endSoundRef = useRef(null)

  useEffect(() => {
    if (enableSound) {
      warningSoundRef.current = new Audio(
        '/The-Quiz-Platform/sounds/tictak.mp3',
      )
      endSoundRef.current = new Audio(
        '/The-Quiz-Platform/sounds/bell-sound.mp3',
      )
    }

    return () => {
      warningSoundRef.current?.pause()
      endSoundRef.current?.pause()
      if (warningTimeoutRef.current) {
        clearTimeout(warningTimeoutRef.current)
      }
    }
  }, [enableSound])

  useEffect(() => {
    setTimeLeft(duration)
    hasEnded.current = false
    hasPlayedWarning.current = false

    if (warningTimeoutRef.current) {
      clearTimeout(warningTimeoutRef.current)
      warningTimeoutRef.current = null
    }
  }, [duration])

  useEffect(() => {
    if (timeLeft <= 0) {
      if (!hasEnded.current) {
        hasEnded.current = true

        if (warningSoundRef.current) {
          warningSoundRef.current.pause()
          warningSoundRef.current.currentTime = 0
          warningSoundRef.current.loop = false
        }

        if (warningTimeoutRef.current) {
          clearTimeout(warningTimeoutRef.current)
          warningTimeoutRef.current = null
        }

        if (enableSound && endSoundRef.current) {
          endSoundRef.current.currentTime = 0
          endSoundRef.current
            .play()
            .catch((e) => console.log('Audio error:', e))
        }

        onTimeEnd?.()
      }
      return
    }

    if (isLobby && enableSound && warningSoundRef.current) {
      const shouldPlay = timeLeft <= lobbyWarningThreshold && timeLeft > 0

      if (shouldPlay && !warningSoundRef.current.loop) {
        warningSoundRef.current.loop = true
        warningSoundRef.current.currentTime = 0
        warningSoundRef.current
          .play()
          .catch((e) => console.log('Audio error:', e))
      } else if (!shouldPlay && warningSoundRef.current.loop) {
        warningSoundRef.current.loop = false
        warningSoundRef.current.pause()
        warningSoundRef.current.currentTime = 0
      }
    }

    if (!isLobby) {
      const warningThreshold = WARNING_TIME
      const shouldPlayWarning =
        timeLeft <= warningThreshold && !hasPlayedWarning.current

      if (shouldPlayWarning && enableSound && warningSoundRef.current) {
        warningSoundRef.current.loop = false
        warningSoundRef.current.currentTime = 0
        warningSoundRef.current
          .play()
          .catch((e) => console.log('Audio error:', e))
        hasPlayedWarning.current = true

        warningTimeoutRef.current = setTimeout(() => {
          if (warningSoundRef.current && !warningSoundRef.current.paused) {
            warningSoundRef.current.pause()
            warningSoundRef.current.currentTime = 0
          }
          warningTimeoutRef.current = null
        }, 10000)
      }
    }

    const timer = setTimeout(() => {
      setTimeLeft((prev) => prev - 1)
    }, 1000)

    return () => clearTimeout(timer)
  }, [timeLeft, onTimeEnd, enableSound, isLobby, lobbyWarningThreshold])

  const isWarningActive = isLobby
    ? timeLeft <= lobbyWarningThreshold && timeLeft > 0
    : timeLeft <= WARNING_TIME && timeLeft > 0

  return {
    timeLeft,
    isWarning: isWarningActive,
  }
}
