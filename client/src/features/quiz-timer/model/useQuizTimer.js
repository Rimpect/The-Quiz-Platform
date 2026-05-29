import { useEffect, useState } from 'react'

const WARNING_TIME = 10

export function useQuizTimer({ duration, onTimeEnd, warningSound }) {
  const [timeLeft, setTimeLeft] = useState(duration)

  useEffect(() => {
    setTimeLeft(duration)
  }, [duration])

  useEffect(() => {
    if (timeLeft <= 0) {
      onTimeEnd?.()
      return
    }

    if (timeLeft === WARNING_TIME && warningSound) {
      warningSound.play()
    }

    const timer = setTimeout(() => {
      setTimeLeft((prev) => prev - 1)
    }, 1000)

    return () => clearTimeout(timer)
  }, [timeLeft, onTimeEnd, warningSound])

  return {
    timeLeft,
    isWarning: timeLeft <= WARNING_TIME,
  }
}
