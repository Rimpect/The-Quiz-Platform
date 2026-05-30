import { useEffect, useRef, useState } from 'react'

const WARNING_TIME = 10

export function useQuizTimer({ duration, onTimeEnd, warningSound }) {
  const [timeLeft, setTimeLeft] = useState(duration)

  const hasEnded = useRef(false)

  useEffect(() => {
    setTimeLeft(duration)
    hasEnded.current = false
  }, [duration])

  useEffect(() => {
    if (timeLeft <= 0) {
      if (!hasEnded.current) {
        hasEnded.current = true
        onTimeEnd?.()
      }

      return
    }

    if (timeLeft === WARNING_TIME && warningSound) {
      warningSound.play()
    }

    const timer = setTimeout(() => {
      setTimeLeft((prev) => prev - 1)
    }, 1000)

    return () => clearTimeout(timer)
  }, [timeLeft])

  return {
    timeLeft,
    isWarning: timeLeft <= WARNING_TIME,
  }
}
