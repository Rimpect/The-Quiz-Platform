import { Button } from '@shared'
import { Save } from 'lucide-react'
import { toast } from 'sonner'

import { saveQuiz } from '../model/saveQuiz'

export function SaveQuiz({ quizData }) {
  const handleSave = async () => {
    try {
      await saveQuiz(quizData)

      toast.success('Квиз сохранен')
    } catch (e) {
      toast.error(e.message)
    }
  }

  return (
    <Button
      onClick={handleSave}
      variant="black"
      size="medium"
      icon={<Save size={20} />}
    >
      Сохранить квиз
    </Button>
  )
}
