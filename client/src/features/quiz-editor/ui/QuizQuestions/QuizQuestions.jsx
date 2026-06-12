import React from 'react'

import { Input, Textarea, Button, Select } from '@shared'
import { Plus, Trash2, X, Clock, Award } from 'lucide-react'
import { toast } from 'sonner'

import { useQuizStore } from '../../model/quiz.store'

import { QuestionMedia } from './QuestionMedia'
import styles from './QuizQuestion.module.scss'

const MAX_ANSWERS = 10

export function QuizQuestions() {
  const questions = useQuizStore((state) => state.quiz.questions)

  const addQuestion = useQuizStore((state) => state.addQuestion)

  const deleteQuestion = useQuizStore((state) => state.deleteQuestion)

  const updateQuestion = useQuizStore((state) => state.updateQuestion)

  const addAnswer = useQuizStore((state) => state.addAnswer)

  const removeAnswer = useQuizStore((state) => state.removeAnswer)

  const updateAnswerText = useQuizStore((state) => state.updateAnswerText)

  const setCorrectAnswer = useQuizStore((state) => state.setCorrectAnswer)

  const toggleCorrectAnswer = useQuizStore((state) => state.toggleCorrectAnswer)

  const setQuestionType = useQuizStore((state) => state.setQuestionType)

  const handleCorrectAnswerToggle = (
    questionId,
    answerId,
    isCurrentlyCorrect,
  ) => {
    if (isCurrentlyCorrect) {
      setCorrectAnswer(questionId, null)
    } else {
      setCorrectAnswer(questionId, answerId)
    }
  }

  const handleAddAnswer = (question) => {
    if (question.answers.length >= MAX_ANSWERS) {
      toast.error(`Максимум ${MAX_ANSWERS} вариантов`)
      return
    }
    addAnswer(question.id)
  }

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
          <div
            key={question.id}
            id={`quiz-question-${index}`}
            className={styles.questionCard}
          >
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
                maxLength={100}
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
              <span className={styles.timeLimitLabel}>
                Время на ответ (сек):
              </span>
              <Input
                type="number"
                value={question.timeLimitSeconds}
                min={0}
                max={300}
                step={5}
                placeholder="0 = без лимита"
                className={styles.timeLimitInput}
                onChange={(e) =>
                  updateQuestion(
                    question.id,
                    'timeLimitSeconds',
                    Number(e.target.value),
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
                  updateQuestion(
                    question.id,
                    'points',
                    Number(e.target.value) || 1,
                  )
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
                  onClick={() => handleAddAnswer(question)}
                >
                  Добавить вариант
                </Button>
              </div>

              <div className={styles.answersList}>
                {question.answers.map((answer, answerIndex) => (
                  <div
                    key={answer.id}
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
                            onChange={() =>
                              toggleCorrectAnswer(question.id, answer.id)
                            }
                          />
                          <span className={styles.checkboxCustom} />
                        </label>
                      ) : (
                        <label className={styles.radioControl}>
                          <input
                            type="radio"
                            name={`question-${question.id}`}
                            checked={answer.isCorrect}
                            onChange={() =>
                              handleCorrectAnswerToggle(
                                question.id,
                                answer.id,
                                answer.isCorrect,
                              )
                            }
                          />
                          <span className={styles.radioCustom} />
                        </label>
                      )}
                    </div>

                    <div className={styles.answerIndex}>{answerIndex + 1}</div>

                    <Input
                      type="text"
                      value={answer.text}
                      maxLength={40}
                      onChange={(e) =>
                        updateAnswerText(question.id, answer.id, e.target.value)
                      }
                      placeholder={`Вариант ${answerIndex + 1}`}
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
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
