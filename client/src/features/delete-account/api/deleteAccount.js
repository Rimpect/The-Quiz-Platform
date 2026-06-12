import { client } from '@shared/api/client'

export async function deleteAccount() {
  return client('/users/me', { method: 'DELETE' })
}
