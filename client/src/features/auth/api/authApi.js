export const login = (data) =>
  request('/auth/login', {
    method: 'POST',
    body: JSON.stringify(data),
  })

export const logout = () =>
  request('/auth/logout', {
    method: 'POST',
  })

export const refreshToken = () =>
  request('/auth/refresh', {
    method: 'POST',
  })

export const getSessions = () => request('/auth/sessions')

export const getHistory = () => request('/auth/history')
