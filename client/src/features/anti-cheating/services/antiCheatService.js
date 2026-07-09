import { IS_DEMO } from '@shared'

class AntiCheatService {
  async submitViolations(quizId, violations) {
    // В демо-режиме нет бэкенда — отправлять нарушения некуда.
    if (IS_DEMO) return
    try {
      const response = await fetch(`/api/quizzes/${quizId}/violations`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          violations,
          timestamp: Date.now(),
          userAgent: navigator.userAgent,
        }),
      })

      if (!response.ok) {
        throw new Error('Failed to submit violations')
      }

      return await response.json()
    } catch (error) {
      console.error('Failed to submit violations:', error)
    }
  }

  startHeartbeat(sessionId, interval = 5000, onViolation) {
    // В демо-режиме heartbeat не нужен (нет сервера сессий).
    if (IS_DEMO) return () => {}
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    let violations = []

    const intervalId = setInterval(async () => {
      try {
        const response = await fetch(
          `/api/quiz-session/${sessionId}/heartbeat`,
          {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              timestamp: Date.now(),
              isTabActive: document.visibilityState === 'visible',
            }),
          },
        )

        const data = await response.json()

        if (data.hasViolations && onViolation) {
          onViolation(data.violations)
        }
      } catch (error) {
        console.error('Heartbeat failed:', error)
      }
    }, interval)

    return () => clearInterval(intervalId)
  }
}

export const antiCheatService = new AntiCheatService()
