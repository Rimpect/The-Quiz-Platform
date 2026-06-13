import { useEffect, useRef } from 'react'

import { useAuthStore } from '@entities'

/**
 * @param {string|null} sessionId
 * @param {(state: object) => void} onState
 */
export function useGameSocket(sessionId, onState) {
  const onStateRef = useRef(onState)
  useEffect(() => {
    onStateRef.current = onState
  }, [onState])

  useEffect(() => {
    if (!sessionId) return

    const token = useAuthStore.getState().token
    if (!token) return

    let ws = null
    let hbTimer = null
    let reconnectTimer = null
    let closedByUs = false
    let attempts = 0

    const connect = () => {
      const proto = window.location.protocol === 'https:' ? 'wss' : 'ws'
      const url = `${proto}://${window.location.host}/api/game/ws/${sessionId}?token=${token}`
      ws = new WebSocket(url)

      ws.onopen = () => {
        attempts = 0
        hbTimer = setInterval(() => {
          try {
            ws.send('ping')
          } catch {
            // сокет закрылся — heartbeat остановится в onclose
          }
        }, 3000)
      }

      ws.onmessage = (event) => {
        try {
          onStateRef.current?.(JSON.parse(event.data))
        } catch {
          // игнорируем некорректные сообщения
        }
      }

      ws.onclose = () => {
        clearInterval(hbTimer)
        if (closedByUs) return
        const delay = Math.min(1000 * 2 ** attempts, 10000)
        attempts += 1
        reconnectTimer = setTimeout(connect, delay)
      }

      ws.onerror = () => {
        try {
          ws.close()
        } catch {
          // no-op
        }
      }
    }

    connect()

    return () => {
      closedByUs = true
      clearInterval(hbTimer)
      clearTimeout(reconnectTimer)
      try {
        ws?.close()
      } catch {
        // no-op
      }
    }
  }, [sessionId])
}
