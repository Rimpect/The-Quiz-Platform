import { z } from 'zod'

export const registerSchema = z
  .object({
    name: z.string().min(2, 'Минимум 2 символа'),
    email: z.email('Некорректный email'),
    password: z.string().min(6, 'Минимум 6 символов'),
    confirmPassword: z.string(),
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: 'Пароли не совпадают',
    path: ['confirmPassword'],
  })
