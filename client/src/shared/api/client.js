import { API_URL } from '../config/env'

const getToken = () => {
  const s = localStorage.getItem('auth-storage')
  return s ? JSON.parse(s)?.state?.token : null
}

// Обновляем токен прямо в persisted-localStorage (формат zustand persist),
// не трогая инстанс стора — чтобы исключить любые конфликты модулей.
const writeToken = (token) => {
  try {
    const s = localStorage.getItem('auth-storage')
    if (!s) return
    const parsed = JSON.parse(s)
    parsed.state = { ...parsed.state, token }
    localStorage.setItem('auth-storage', JSON.stringify(parsed))
  } catch {
    /* ignore */
  }
}

// Один общий refresh на все параллельные 401, чтобы не дёргать /refresh пачкой
let refreshPromise = null

const doRefresh = async () => {
  try {
    const res = await fetch(`${API_URL}/auth/refresh`, {
      method: 'POST',
      credentials: 'include', // отправляет httpOnly refresh-cookie
    })
    if (!res.ok) return null
    const json = await res.json()
    const token = (json?.data ?? json)?.access_token
    if (token) writeToken(token)
    return token || null
  } catch {
    return null
  }
}

export const client = async (endpoint, options = {}, _retry = false) => {
  const token = getToken()

  // Для FormData НЕ ставим Content-Type — браузер сам выставит multipart с boundary
  const isFormData = options.body instanceof FormData

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    credentials: 'include',
    headers: {
      ...(isFormData ? {} : { 'Content-Type': 'application/json' }),
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    },
  })

  // Access истёк (401) → пробуем обновить по refresh-токену и повторить запрос
  const isAuthCall = endpoint.includes('/auth/')
  if (response.status === 401 && !_retry && token && !isAuthCall) {
    if (!refreshPromise) {
      refreshPromise = doRefresh().finally(() => {
        refreshPromise = null
      })
    }
    const newToken = await refreshPromise
    if (newToken) {
      return client(endpoint, options, true) // повтор с новым access-токеном
    }
  }

  const data = await response.json()

  if (!response.ok) {
    throw new Error(data?.message || data?.detail || 'API Error')
  }

  // Сервер оборачивает все ответы в { data, status_code, message } через ResponseFormatterMiddleware
  return data?.data !== undefined ? data.data : data
}
