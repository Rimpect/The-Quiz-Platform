import { Input, Textarea, Button, Select } from '@shared'
import { Plus, Trash2, Clock, Award } from 'lucide-react'
import { toast } from 'sonner'

import { useQuizStore } from '../../model/quiz.store'

import { AnswerRow } from './AnswerRow'
import { QuestionMedia } from './QuestionMedia'
import styles from './QuizQuestion.module.scss'

const MAX_ANSWERS = 10

export function QuestionCard({ question, index }) {
  const deleteQuestion = useQuizStore((s) => s.deleteQuestion)
  const updateQuestion = useQuizStore((s) => s.updateQuestion)
  const addAnswer = useQuizStore((s) => s.addAnswer)
  const setQuestionType = useQuizStore((s) => s.setQuestionType)

  const handleAddAnswer = () => {
    if (question.answers.length >= MAX_ANSWERS) {
      toast.error(`Максимум ${MAX_ANSWERS} вариантов`)
      return
    }
    addAnswer(question.id)
  }

  return (
    <div id={`quiz-question-${index}`} className={styles.questionCard}>
      <div className={styles.questionCardHeader}>
        <div className={styles.questionNumber}>Вопрос {index + 1}</div>

        <Button
          variant="transparent"
          size="medium"
          icon={<Trash2 size={20} color="red" />}
          type="button"
          onClick={() => deleteQuestion(question.id)}
        />
      </div>

      <QuestionMedia
        mediaUrl={question.mediaUrl}
        onUpload={(url) => updateQuestion(question.id, 'mediaUrl', url)}
      />

      <div className={styles.questionTextField}>
        <div className={styles.fieldLabel}>Текст вопроса *</div>

        <Textarea
          value={question.questionText}
          maxLength={300}
          onChange={(e) =>
            updateQuestion(question.id, 'questionText', e.target.value)
          }
          className={styles.questionTextarea}
        />
      </div>

      <div className={styles.questionTextField}>
        <div className={styles.fieldLabel}>Тип ответа</div>

        <Select
          value={question.questionType || 'single'}
          onChange={(e) => setQuestionType(question.id, e.target.value)}
        >
          <option value="single">Одиночный выбор</option>
          <option value="multiple">Множественный выбор</option>
        </Select>
      </div>

      <div className={styles.timeLimitRow}>
        <Clock size={16} className={styles.timeLimitIcon} />
        <span className={styles.timeLimitLabel}>Время на ответ (сек):</span>
        <Input
          type="number"
          value={question.timeLimitSeconds || ''}
          min={0}
          max={300}
          step={5}
          placeholder="0 = без лимита"
          className={styles.timeLimitInput}
          onChange={(e) =>
            updateQuestion(
              question.id,
              'timeLimitSeconds',
              Number(e.target.value) || 0,
            )
          }
        />
      </div>

      <div className={styles.timeLimitRow}>
        <Award size={16} className={styles.timeLimitIcon} />
        <span className={styles.timeLimitLabel}>
          Баллов за правильный ответ:
        </span>
        <Input
          type="number"
          value={question.points}
          min={1}
          max={100}
          className={styles.timeLimitInput}
          onChange={(e) =>
            updateQuestion(question.id, 'points', Number(e.target.value) || 1)
          }
        />
      </div>

      <div className={styles.answersSection}>
        <div className={styles.answersHeader}>
          <div className={styles.fieldLabel}>Варианты ответов *</div>

          <Button
            variant="black"
            size="medium"
            icon={<Plus size={20} />}
            type="button"
            disabled={question.answers.length >= MAX_ANSWERS}
            onClick={handleAddAnswer}
          >
            Добавить вариант
          </Button>
        </div>

        <div className={styles.answersList}>
          {question.answers.map((answer, answerIndex) => (
            <AnswerRow
              key={answer.id}
              question={question}
              answer={answer}
              index={answerIndex}
            />
          ))}
        </div>
      </div>
    </div>
  )
}
