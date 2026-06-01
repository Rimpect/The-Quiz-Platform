import { z } from 'zod'
// Добавляем схему для пользователя (из базы данных)
export const userSchema = z.object({
  id: z.number(),
  name: z.string().min(2, 'Минимум 2 символа'),
  email: z.string().email('Некорректный email'),
  role: z.enum(['user', 'admin']),
  avatar: z.string().nullable().optional(),
  createdAt: z.string().optional(),
})

// Вспомогательная функция для валидации пользователя
export const validateUser = (data) => {
  const result = userSchema.safeParse(data)
  if (!result.success) {
    return { isValid: false, error: result.error.issues[0].message }
  }
  return { isValid: true, error: null, data: result.data }
}
