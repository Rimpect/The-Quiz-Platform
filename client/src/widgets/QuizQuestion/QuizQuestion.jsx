import React, { useState } from 'react'

import { Input, Textarea } from '@shared'

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
    <div className={styles.quizBuilder}>
      <div className={styles.headerBar}>
        <h2 className={styles.headerTitle}>Вопросы</h2>
        <button
          type="button"
          onClick={addQuestion}
          className={styles.addQuestionBtn}
        >
          + Добавить вопрос
        </button>
      </div>

      {questions.map((question, index) => (
        <div key={question.id} className={styles.questionCard}>
          <div className={styles.questionCardHeader}>
            <div className={styles.questionNumber}>Вопрос {index + 1}</div>
            <button
              type="button"
              onClick={() => deleteQuestion(question.id)}
              className={styles.deleteQuestionBtn}
              disabled={questions.length <= 1}
            >
              ✕ Удалить вопрос
            </button>
          </div>

          <div className={styles.questionSettings}>
            <div className={styles.typeSelector}>
              <div className={styles.fieldLabel}>Тип вопроса</div>
              <div className={styles.typeButtons}>
                <button
                  type="button"
                  className={`${styles.typeBtn} ${question.questionType === 'single' ? styles.typeBtnActive : ''}`}
                  onClick={() =>
                    handleQuestionTypeChange(question.id, 'single')
                  }
                >
                  Один ответ
                </button>
                <button
                  type="button"
                  className={`${styles.typeBtn} ${question.questionType === 'multiple' ? styles.typeBtnActive : ''}`}
                  onClick={() =>
                    handleQuestionTypeChange(question.id, 'multiple')
                  }
                >
                  Несколько ответов
                </button>
              </div>
            </div>

            <div className={styles.pointsField}>
              <div className={styles.fieldLabel}>Баллы за ответ</div>
              <Input
                type="number"
                value={question.points}
                onChange={(e) =>
                  updateQuestion(question.id, 'points', Number(e.target.value))
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
              <button type="button" className={styles.mediaBtn}>
                📷 Загрузить изображение
              </button>
              <button type="button" className={styles.mediaBtn}>
                🎥 Загрузить видео
              </button>
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
              <button
                type="button"
                onClick={() => addAnswer(question.id)}
                className={styles.addAnswerBtn}
              >
                + Добавить вариант
              </button>
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

                  <button
                    type="button"
                    onClick={() => removeAnswer(question.id, answer.id)}
                    className={styles.removeAnswerBtn}
                    disabled={question.answers.length <= 2}
                  >
                    ✕
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}
