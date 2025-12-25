import React, { useState, useEffect } from "react";
import { AverageButton } from "../../shared/Buttons/AverageButton/AverageButton";
import { useParams } from "react-router-dom";
import "./Quiz.css";
import { Link } from "react-router-dom";

export function Quiz() {
  const { id } = useParams();
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [timer, setTimer] = useState(30);
  const [score, setScore] = useState(0);
  const [isFinished, setIsFinished] = useState(false);

  // Минимальные тестовые вопросы с вариантами ответов
  const questions = [
    {
      question: "Вопрос 1",
      answers: ["Ответ 1", "Ответ 2", "Ответ 3", "Ответ 4"],
      correctAnswer: 0
    },
    {
      question: "Вопрос 2",
      answers: ["Ответ A", "Ответ B", "Ответ C", "Ответ D"],
      correctAnswer: 1
    },
    {
      question: "Вопрос 3",
      answers: ["Вариант 1", "Вариант 2", "Вариант 3", "Вариант 4"],
      correctAnswer: 2
    },
    {
      question: "Вопрос 4",
      answers: ["Выбор 1", "Выбор 2", "Выбор 3", "Выбор 4"],
      correctAnswer: 3
    },
    {
      question: "Вопрос 5",
      answers: ["Опция 1", "Опция 2", "Опция 3", "Опция 4"],
      correctAnswer: 0
    },
    {
      question: "Вопрос 6",
      answers: ["Результат 1", "Результат 2", "Результат 3", "Результат 4"],
      correctAnswer: 1
    },
    {
      question: "Вопрос 7",
      answers: ["Тест 1", "Тест 2", "Тест 3", "Тест 4"],
      correctAnswer: 2
    },
    {
      question: "Вопрос 8",
      answers: ["Пункт 1", "Пункт 2", "Пункт 3", "Пункт 4"],
      correctAnswer: 3
    },
    {
      question: "Вопрос 9",
      answers: ["Элемент 1", "Элемент 2", "Элемент 3", "Элемент 4"],
      correctAnswer: 0
    },
    {
      question: "Вопрос 10",
      answers: ["Итог 1", "Итог 2", "Итог 3", "Итог 4"],
      correctAnswer: 1
    }
  ];

  // Таймер обратного отсчета
  useEffect(() => {
    if (timer > 0 && !isFinished && currentQuestion < questions.length) {
      const interval = setInterval(() => {
        setTimer((prevTimer) => prevTimer - 1);
      }, 1000);
      return () => clearInterval(interval);
    } else if (timer === 0) {
      handleNextQuestion();
    }
  }, [timer, isFinished, currentQuestion]);

  // Обработчик выбора ответа
  const handleAnswerSelect = (selectedIndex) => {
    if (selectedIndex === questions[currentQuestion].correctAnswer) {
      setScore(score + 1);
    }
    handleNextQuestion();
  };

  // Переход к следующему вопросу
  const handleNextQuestion = () => {
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
      setTimer(30);
    } else {
      setIsFinished(true);
    }
  };

  // Преждевременное завершение квиза
  const handleFinishQuiz = () => {
    setIsFinished(true);
  };

  if (isFinished) {
    return (
      <div className="container_quiz">
        <div className="container_question">
          <h2>Квиз завершен!</h2>
          <div>Квиз № {id}</div>
        </div>
        <div className="answer">
          <h3>Ваш результат: {score} из {questions.length}</h3>
        </div>
        <Link to={`/`}>
          <AverageButton>Вернуться на главную</AverageButton>
        </Link>
      </div>
    );
  }

  return (
    <div className="container_quiz">
      <div className="container_question">
        <div className="question">
          <h2>{questions[currentQuestion].question}</h2>
          <p>Вопрос {currentQuestion + 1} из {questions.length}</p>
        </div>
        <div className="Timer">
          <h3>Таймер: {timer} сек</h3>
        </div>
        <div>Квиз № {id}</div>
        <div>Счет: {score}</div>
      </div>
      
      <div className="answer">
        <h3>Варианты ответов:</h3>
        <div className="answers-container">
          {questions[currentQuestion].answers.map((answer, index) => (
            <div 
              key={index} 
              className="answer-option"
              onClick={() => handleAnswerSelect(index)}
              style={{
                cursor: 'pointer',
                padding: '10px',
                margin: '5px',
                border: '1px solid #ccc',
                borderRadius: '5px'
              }}
            >
              {answer}
            </div>
          ))}
        </div>
      </div>

      <div>
        <p>Таблица лидеров для закрытого квиза</p>
        <p>Места участников в данный момент</p>
      </div>

      <div className="aaaaa">
        <AverageButton onClick={() => handleNextQuestion()}>
          Пропустить вопрос
        </AverageButton>
        <AverageButton onClick={handleFinishQuiz}>
          Преждевременно закончить квиз
        </AverageButton>
        <Link to={`/`}>
          <AverageButton>Выйти в главное меню</AverageButton>
        </Link>
      </div>
    </div>
  );
}