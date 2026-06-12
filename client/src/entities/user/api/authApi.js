import { client } from '@shared/api/client'
import { endpoints } from '@shared/api/endpoints'

export const registerUser = async ({ name, email, password }) => {
  return client(endpoints.users.base, {
    method: 'POST',
    body: JSON.stringify({ nickname: name, email, password }),
  })
}
