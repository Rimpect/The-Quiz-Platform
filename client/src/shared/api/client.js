import { API_URL } from '../config/env'

const getToken = () => {
  const s = localStorage.getItem('auth-storage')
  return s ? JSON.parse(s)?.state?.token : null
}

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

// Сброс протухшей авторизации: чистим localStorage и уведомляем приложение,
// чтобы шапка/гварды сразу отразили выход (например, после рестарта сервера).
const clearStoredAuth = () => {
  try {
    const s = localStorage.getItem('auth-storage')
    if (s) {
      const parsed = JSON.parse(s)
      parsed.state = {
        ...parsed.state,
        token: null,
        refreshToken: null,
        user: null,
        isAuthenticated: false,
      }
      localStorage.setItem('auth-storage', JSON.stringify(parsed))
    }
  } catch {
    /* ignore */
  }
  window.dispatchEvent(new Event('auth:expired'))
}

let refreshPromise = null

const doRefresh = async () => {
  try {
    const res = await fetch(`${API_URL}/auth/refresh`, {
      method: 'POST',
      credentials: 'include',
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
    // refresh не удался (токен протух / сервер перезапущен) → разлогиниваем
    clearStoredAuth()
  }

  const data = await response.json()

  if (!response.ok) {
    throw new Error(data?.message || data?.detail || 'API Error')
  }

  // Сервер оборачивает все ответы в { data, status_code, message } через ResponseFormatterMiddleware
  return data?.data !== undefined ? data.data : data
}
