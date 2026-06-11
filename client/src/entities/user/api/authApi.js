import { request } from '@shared'

export const loginUser = async ({ email, password }) => {
  const users = await request(`/users?email=${encodeURIComponent(email)}`)
  if (!Array.isArray(users)) {
    return []
  }

  return users.filter((user) => user.password === password)
}

export const registerUser = async ({ name, email, password }) => {
  const exists = await request(`/users?email=${encodeURIComponent(email)}`)
  if (Array.isArray(exists) && exists.length > 0) {
    throw new Error('Пользователь с таким email уже зарегистрирован')
  }

  const payload = {
    name,
    email,
    password,
    role: 'user',
    avatar: null,
  }

  return request('/users', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}
