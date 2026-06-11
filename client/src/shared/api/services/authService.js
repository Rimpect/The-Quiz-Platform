import { client } from '../client'
import { endpoints } from '../endpoints'

export const authService = {
  login: (credentials) =>
    client(endpoints.auth.login, {
      method: 'POST',
      body: JSON.stringify(credentials),
    }),

  logout: () =>
    client(endpoints.auth.logout, {
      method: 'POST',
    }),

  logoutAll: () =>
    client(endpoints.auth.logoutAll, {
      method: 'POST',
    }),

  refresh: () =>
    client(endpoints.auth.refresh, {
      method: 'POST',
    }),

  revokeAccess: () =>
    client(endpoints.auth.revokeAccess, {
      method: 'POST',
    }),

  getSessions: () =>
    client(endpoints.auth.sessions, {
      method: 'GET',
    }),

  getHistory: () =>
    client(endpoints.auth.history, {
      method: 'GET',
    }),
}
