import { request } from '@shared'

export const getUsers = () => request('/users')

export const getCurrentUser = () => request('/users/me')

export const getUserById = (id) => request(`/users/${id}`)

export const updateCurrentUser = (data) =>
  request('/users/me', {
    method: 'PUT',
    body: JSON.stringify(data),
  })

export const getUserStatistics = () => request('/users/me/statistics')
