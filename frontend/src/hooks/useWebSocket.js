import { useEffect, useRef, useCallback } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { addNotification } from '../features/notifications/notificationSlice'

const WS_BASE = import.meta.env.VITE_WS_URL || 'ws://localhost:8000'

export default function useWebSocket() {
  const ws = useRef(null)
  const dispatch = useDispatch()
  const { tokens } = useSelector((state) => state.auth)
  const reconnectTimeout = useRef(null)

  const connect = useCallback(() => {
    if (!tokens?.access) return

    const url = `${WS_BASE}/ws/notifications/?token=${tokens.access}`
    ws.current = new WebSocket(url)

    ws.current.onopen = () => {
      console.log('WebSocket connected')
    }

    ws.current.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        if (data.type === 'notification') {
          dispatch(addNotification(data.notification))
        } else if (data.type === 'security_alert') {
          console.warn('Security alert:', data.alert)
        }
      } catch (err) {
        console.error('WebSocket message error:', err)
      }
    }

    ws.current.onclose = (event) => {
      if (event.code !== 4001) {
        reconnectTimeout.current = setTimeout(connect, 5000)
      }
    }

    ws.current.onerror = (err) => {
      console.error('WebSocket error:', err)
      ws.current?.close()
    }
  }, [tokens, dispatch])

  useEffect(() => {
    connect()
    const pingInterval = setInterval(() => {
      if (ws.current?.readyState === WebSocket.OPEN) {
        ws.current.send(JSON.stringify({ type: 'ping' }))
      }
    }, 30000)

    return () => {
      clearInterval(pingInterval)
      clearTimeout(reconnectTimeout.current)
      ws.current?.close()
    }
  }, [connect])

  return ws
}
