import React, { useState } from 'react'

import { Input, Textarea, Button } from '@shared'
import { Plus, Trash2, Image, Video, Music, X } from 'lucide-react'
import styles from './QuizQuestion.module.scss'

export function QuizQuestion() {
  const [questions, setQuestions] = useState([
    {
      id: 1,
      questionType: 'single',
      points: 1,
      questionText: '',
      answers: [
        { id: 1, text: '', isCorrect: false },
        { id: 2, text: '', isCorrect: false },
        { id: 3, text: '', isCorrect: false },
        { id: 4, text: '', isCorrect: false },
      ],
    },
  ])

  const addQuestion = () => {
    const newId = Math.max(...questions.map((q) => q.id), 0) + 1
    setQuestions([
      ...questions,
      {
        id: newId,
        questionType: 'single',
        points: 1,
        questionText: '',
        answers: [
          { id: 1, text: '', isCorrect: false },
          { id: 2, text: '', isCorrect: false },
          { id: 3, text: '', isCorrect: false },
          { id: 4, text: '', isCorrect: false },
        ],
      },
    ])
  }

  const deleteQuestion = (questionId) => {
    if (questions.length > 1) {
      setQuestions(questions.filter((q) => q.id !== questionId))
    }
  }

  const updateQuestion = (questionId, field, value) => {
    setQuestions(
      questions.map((q) =>
        q.id === questionId ? { ...q, [field]: value } : q,
      ),
    )
  }

  const addAnswer = (questionId) => {
    setQuestions(
      questions.map((q) => {
        if (q.id === questionId) {
          const newId = Math.max(...q.answers.map((a) => a.id), 0) + 1
          return {
            ...q,
            answers: [...q.answers, { id: newId, text: '', isCorrect: false }],
          }
        }
        return q
      }),
    )
  }

  const removeAnswer = (questionId, answerId) => {
    setQuestions(
      questions.map((q) => {
        if (q.id === questionId && q.answers.length > 2) {
          return {
            ...q,
            answers: q.answers.filter((a) => a.id !== answerId),
          }
        }
        return q
      }),
    )
  }

  const updateAnswerText = (questionId, answerId, text) => {
    setQuestions(
      questions.map((q) => {
        if (q.id === questionId) {
          return {
            ...q,
            answers: q.answers.map((a) =>
              a.id === answerId ? { ...a, text } : a,
            ),
          }
        }
        return q
      }),
    )
  }

  const updateAnswerCorrect = (questionId, answerId, isCorrect) => {
    setQuestions(
      questions.map((q) => {
        if (q.id === questionId) {
          let newAnswers
          if (q.questionType === 'single') {
            newAnswers = q.answers.map((a) => ({
              ...a,
              isCorrect: a.id === answerId ? isCorrect : false,
            }))
          } else {
            newAnswers = q.answers.map((a) =>
              a.id === answerId ? { ...a, isCorrect } : a,
            )
          }
          return { ...q, answers: newAnswers }
        }
        return q
      }),
    )
  }

  const handleQuestionTypeChange = (questionId, type) => {
    setQuestions(
      questions.map((q) => {
        if (q.id === questionId) {
          let newAnswers = q.answers
          if (type === 'single') {
            newAnswers = q.answers.map((a, idx) => ({
              ...a,
              isCorrect: idx === 0 ? a.isCorrect : false,
            }))
          }
          return { ...q, questionType: type, answers: newAnswers }
        }
        return q
      }),
    )
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
          <div key={question.id} className={styles.questionCard}>
            <div className={styles.questionCardHeader}>
              <div className={styles.questionNumber}>Вопрос {index + 1}</div>
              <Button
                variant="red"
                size="medium"
                icon={<Trash2 size={20} />}
                type="button"
                onClick={() => deleteQuestion(question.id)}
                disabled={questions.length <= 1}
              ></Button>
            </div>

            <div className={styles.questionSettings}>
              <div className={styles.typeSelector}>
                <div className={styles.fieldLabel}>Тип вопроса</div>
                <div className={styles.typeButtons}>
                  <Button
                    className={`${styles.typeBtn} ${question.questionType === 'single' ? styles.typeBtnActive : ''}`}
                    type="button"
                    onClick={() =>
                      handleQuestionTypeChange(question.id, 'single')
                    }
                  >
                    Один ответ
                  </Button>
                  <Button
                    type="button"
                    className={`${styles.typeBtn} ${question.questionType === 'multiple' ? styles.typeBtnActive : ''}`}
                    onClick={() =>
                      handleQuestionTypeChange(question.id, 'multiple')
                    }
                  >
                    Несколько ответов
                  </Button>
                </div>
              </div>

              <div className={styles.pointsField}>
                <div className={styles.fieldLabel}>Баллы за ответ</div>
                <Input
                  type="number"
                  value={question.points}
                  onChange={(e) =>
                    updateQuestion(
                      question.id,
                      'points',
                      Number(e.target.value),
                    )
                  }
                  min={1}
                  step={1}
                  className={styles.pointsInput}
                />
              </div>
            </div>

            <div className={styles.mediaSection}>
              <div className={styles.fieldLabel}>Добавить медиа</div>
              <div className={styles.mediaButtons}>
                <Button
                  variant="white"
                  size="medium"
                  icon={<Image size={20} />}
                  type="button"
                >
                  картинка
                </Button>
                <Button
                  variant="white"
                  size="medium"
                  icon={<Video size={20} />}
                  type="button"
                >
                  Видео
                </Button>
                <Button
                  variant="white"
                  size="medium"
                  icon={<Music size={20} />}
                  type="button"
                >
                  Аудио
                </Button>
              </div>
            </div>

            <div className={styles.questionTextField}>
              <div className={styles.fieldLabel}>Текст вопроса *</div>
              <Textarea
                value={question.questionText}
                onChange={(e) =>
                  updateQuestion(question.id, 'questionText', e.target.value)
                }
                placeholder="Введите текст вопроса..."
                rows={3}
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
                  onClick={() => addAnswer(question.id)}
                >
                  Добавить вариант
                </Button>
              </div>

              <div className={styles.answersList}>
                {question.answers.map((answer, answerIndex) => (
                  <div
                    key={answer.id}
                    className={`${styles.answerRow} ${answer.isCorrect ? styles.answerRowCorrect : ''}`}
                  >
                    <div className={styles.correctMarker}>
                      {question.questionType === 'single' ? (
                        <label className={styles.radioControl}>
                          <input
                            type="radio"
                            name={`question-${question.id}-correct`}
                            checked={answer.isCorrect}
                            onChange={(e) =>
                              updateAnswerCorrect(
                                question.id,
                                answer.id,
                                e.target.checked,
                              )
                            }
                          />
                          <span className={styles.radioCustom}></span>
                        </label>
                      ) : (
                        <label className={styles.checkboxControl}>
                          <input
                            type="checkbox"
                            checked={answer.isCorrect}
                            onChange={(e) =>
                              updateAnswerCorrect(
                                question.id,
                                answer.id,
                                e.target.checked,
                              )
                            }
                          />
                          <span className={styles.checkboxCustom}></span>
                        </label>
                      )}
                    </div>

                    <div className={styles.answerIndex}>{answerIndex + 1}</div>

                    <Input
                      type="text"
                      value={answer.text}
                      onChange={(e) =>
                        updateAnswerText(question.id, answer.id, e.target.value)
                      }
                      placeholder={`Вариант ${answerIndex + 1}`}
                      className={styles.answerInput}
                    />
                    <Button
                      className={styles.removeAnswerBtn}
                      size="medium"
                      icon={<X size={20} />}
                      type="button"
                      onClick={() => removeAnswer(question.id, answer.id)}
                      disabled={question.answers.length <= 2}
                    ></Button>
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
