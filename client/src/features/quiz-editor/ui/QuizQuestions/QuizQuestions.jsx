import React from 'react'

import { Input, Textarea, Button } from '@shared'
import { Plus, Trash2, Image, Video, Music, X } from 'lucide-react'

import { useQuizStore } from '../../model/quiz.store'

import styles from './QuizQuestion.module.scss'

export function QuizQuestions() {
  const questions = useQuizStore((state) => state.quiz.questions)

  const addQuestion = useQuizStore((state) => state.addQuestion)

  const deleteQuestion = useQuizStore((state) => state.deleteQuestion)

  const updateQuestion = useQuizStore((state) => state.updateQuestion)

  const addAnswer = useQuizStore((state) => state.addAnswer)

  const removeAnswer = useQuizStore((state) => state.removeAnswer)

  const updateAnswerText = useQuizStore((state) => state.updateAnswerText)

  const setCorrectAnswer = useQuizStore((state) => state.setCorrectAnswer)

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
                variant="transparent"
                size="medium"
                icon={<Trash2 size={20} color="red" />}
                type="button"
                onClick={() => deleteQuestion(question.id)}
              />
            </div>

            <div className={styles.mediaSection}>
              <div className={styles.fieldLabel}>Добавить медиа</div>

              <div className={styles.mediaButtons}>
                <Button
                  variant="white"
                  size="medium"
                  icon={<Image size={20} />}
                >
                  картинка
                </Button>

                <Button
                  variant="white"
                  size="medium"
                  icon={<Video size={20} />}
                >
                  Видео
                </Button>

                <Button
                  variant="white"
                  size="medium"
                  icon={<Music size={20} />}
                >
                  Аудио
                </Button>
              </div>
            </div>

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
                    className={`${styles.answerRow} ${
                      answer.isCorrect ? styles.answerRowCorrect : ''
                    }`}
                  >
                    <div className={styles.correctMarker}>
                      <label className={styles.radioControl}>
                        <input
                          type="radio"
                          checked={answer.isCorrect}
                          onChange={() =>
                            setCorrectAnswer(question.id, answer.id)
                          }
                        />

                        <span className={styles.radioCustom} />
                      </label>
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
                    />

                    <Button
                      className={styles.removeAnswerBtn}
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
