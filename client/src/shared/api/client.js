import { API_URL } from '../config/env'

export const client = async (endpoint, options = {}) => {
  const authStorage = localStorage.getItem('auth-storage')
  const token = authStorage ? JSON.parse(authStorage)?.state?.token : null

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

  const data = await response.json()

  if (!response.ok) {
    throw new Error(data?.message || data?.detail || 'API Error')
  }

  // Сервер оборачивает все ответы в { data, status_code, message } через ResponseFormatterMiddleware
  return data?.data !== undefined ? data.data : data
}
