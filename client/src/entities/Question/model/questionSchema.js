import { z } from 'zod'

const questionSchemaItem = z.object({
  id: z.string(),
  quizId: z.number(),
  question: z.string(),
  questionType: z.enum(['single', 'multiple']),
  mediaType: z.enum(['image', 'audio', 'video']).optional(),
  mediaUrl: z.string().url().optional(),
  options: z.array(z.string()),
  correctAnswers: z.array(z.number()),
  points: z.number(),
})

export const questionSchema = z.array(questionSchemaItem)
