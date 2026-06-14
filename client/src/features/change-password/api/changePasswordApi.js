import { client } from '@shared/api/client'

/**
 * Смена пароля текущего пользователя.
 * @param {{currentPassword: string, newPassword: string}} data — валидированные данные
 */
export async function changePasswordApi(data) {
  return client('/users/me/change-password', {
    method: 'POST',
    body: JSON.stringify({
      current_password: data.currentPassword,
      new_password: data.newPassword,
    }),
  })
}
