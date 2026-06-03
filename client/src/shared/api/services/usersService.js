import { client } from '../client'
import { endpoints } from '../endpoints'

export const usersService = {
  getUsers: () =>
    client(endpoints.users.base, {
      method: 'GET',
    }),

  getUserById: (userId) =>
    client(endpoints.users.byId(userId), {
      method: 'GET',
    }),

  getCurrentUser: () =>
    client(endpoints.users.me, {
      method: 'GET',
    }),

  updateCurrentUser: (data) =>
    client(endpoints.users.me, {
      method: 'PUT',
      body: JSON.stringify(data),
    }),

  deleteCurrentUser: () =>
    client(endpoints.users.me, {
      method: 'DELETE',
    }),

  getStatistics: () =>
    client(endpoints.users.statistics, {
      method: 'GET',
    }),
}
