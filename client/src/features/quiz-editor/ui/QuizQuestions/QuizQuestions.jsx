import { Button } from '@shared'
import { Plus } from 'lucide-react'

import { useQuizStore } from '../../model/quiz.store'

import { QuestionCard } from './QuestionCard'
import styles from './QuizQuestion.module.scss'

export function QuizQuestions() {
  const questions = useQuizStore((state) => state.quiz.questions)
  const addQuestion = useQuizStore((state) => state.addQuestion)

  return (
    <div>
      <div className={styles.headerBar}>
        <h2 className={styles.headerTitle}>Вопросы</h2>

        <Button
          variant="black"
          size="medium"
          icon={<Plus size={20} />}
          type="button"
          onClick={addQuestion}
        >
          Добавить вопрос
        </Button>
      </div>

      <div className={styles.quizBuilder}>
        {questions.map((question, index) => (
          <QuestionCard key={question.id} question={question} index={index} />
        ))}
      </div>
    </div>
  )
}
