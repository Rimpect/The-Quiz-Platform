import { useState } from 'react'

import { changePasswordApi } from '../api/changePasswordApi.js'

import { changePasswordSchema } from './schema/changePasswordSchema.js'

export function useChangePassword() {
  const [loading, setLoading] = useState(false)

  const submit = async (data) => {
    const result = changePasswordSchema.safeParse(data)

    if (!result.success) {
      return {
        ok: false,
        errors: result.error.flatten().fieldErrors,
      }
    }

    setLoading(true)

    try {
      await changePasswordApi(result.data)

      return { ok: true }
    } catch (e) {
      return { ok: false, error: e.message || 'Ошибка изменения пароля' }
    } finally {
      setLoading(false)
    }
  }

  return { submit, loading }
}
