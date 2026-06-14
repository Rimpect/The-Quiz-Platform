import { Input, Button } from '@shared'
import { X } from 'lucide-react'

import { useQuizStore } from '../../model/quiz.store'

import styles from './QuizQuestion.module.scss'

/**
 * Один вариант ответа: маркер правильности (radio для одиночного выбора,
 * checkbox для множественного), поле текста и кнопка удаления.
 */
export function AnswerRow({ question, answer, index }) {
  const updateAnswerText = useQuizStore((s) => s.updateAnswerText)
  const removeAnswer = useQuizStore((s) => s.removeAnswer)
  const setCorrectAnswer = useQuizStore((s) => s.setCorrectAnswer)
  const toggleCorrectAnswer = useQuizStore((s) => s.toggleCorrectAnswer)

  // Одиночный выбор: повторный клик по уже выбранному снимает отметку
  const handleRadioToggle = () =>
    setCorrectAnswer(question.id, answer.isCorrect ? null : answer.id)

  return (
    <div
      className={`${styles.answerRow} ${
        answer.isCorrect ? styles.answerRowCorrect : ''
      }`}
    >
      <div className={styles.correctMarker}>
        {question.questionType === 'multiple' ? (
          <label className={styles.checkboxControl}>
            <input
              type="checkbox"
              checked={answer.isCorrect}
              onChange={() => toggleCorrectAnswer(question.id, answer.id)}
            />
            <span className={styles.checkboxCustom} />
          </label>
        ) : (
          <label className={styles.radioControl}>
            <input
              type="radio"
              name={`question-${question.id}`}
              checked={answer.isCorrect}
              onChange={handleRadioToggle}
            />
            <span className={styles.radioCustom} />
          </label>
        )}
      </div>

      <div className={styles.answerIndex}>{index + 1}</div>

      <Input
        type="text"
        value={answer.text}
        maxLength={150}
        onChange={(e) => updateAnswerText(question.id, answer.id, e.target.value)}
        placeholder={`Вариант ${index + 1}`}
        className={styles.answerInput}
        variant="default"
      />

      <Button
        variant="transparent"
        size="medium"
        icon={<X size={20} />}
        type="button"
        onClick={() => removeAnswer(question.id, answer.id)}
      />
    </div>
  )
}
