import { API_URL } from '../config/env'
import { IS_DEMO } from '../config/isDemo'

export const request = async (endpoint, options = {}) => {
  // В демо-режиме запросы обслуживает локальный mock-роутер (без сети).
  if (IS_DEMO) {
    const { mockRouter } = await import('./mock/mockRouter')
    return mockRouter(endpoint, options)
  }

  const response = await fetch(`${API_URL}${endpoint}`, {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  })

  if (!response.ok) {
    const data = await response.json().catch(() => ({}))
    throw new Error(data?.message || data?.detail || 'Request failed')
  }

  const data = await response.json()
  return data?.data !== undefined ? data.data : data
}
