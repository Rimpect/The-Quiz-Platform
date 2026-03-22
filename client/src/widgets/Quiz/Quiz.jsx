import React, { useState, useEffect } from "react";
import { AverageButton } from "../../shared/Buttons/AverageButton/AverageButton";
import { useParams, useNavigate } from "react-router-dom";
import "./Quiz.scss";
import { Link } from "react-router-dom";
import FinishQuiz from "../../pages/FinishQuiz/FinishQuiz";

export function Quiz() {
  const { id } = useParams();
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState([]);
  const [isAnswered, setIsAnswered] = useState(false);
  const [totalScore, setTotalScore] = useState(0);
  const [maxPossibleScore, setMaxPossibleScore] = useState(0);
  const [correctCount, setCorrectCount] = useState(0);
  const [timeLeft, setTimeLeft] = useState(30);
  const [isFinished, setIsFinished] = useState(false);

  const navigate = useNavigate();
  // Расширенные вопросы с поддержкой разных типов и медиа
  const questions = [
    {
      id: "1",
      question: "Что изображено на этой картине?",
      questionType: "single",
      mediaType: "image",
      mediaUrl:
        "https://images.unsplash.com/photo-1770301380828-3ebc4a260d34?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxmYW1vdXMlMjBwYWludGluZyUyMGFydCUyMG1hc3RlcnBpZWNlfGVufDF8fHx8MTc3MjUzMTY1N3ww&ixlib=rb-4.1.0&q=80&w=1080",
      options: ["Пейзаж", "Портрет", "Натюрморт", "Абстракция"],
      correctAnswers: [0],
      points: 10,
    },
    {
      id: "2",
      question: "Какая планета является самой большой в Солнечной системе?",
      questionType: "single",
      options: ["Марс", "Сатурн", "Юпитер", "Нептун"],
      correctAnswers: [2],
      points: 10,
    },
    {
      id: "3",
      question: "Выберите все столицы европейских стран:",
      questionType: "multiple",
      options: ["Париж", "Токио", "Берлин", "Пекин"],
      correctAnswers: [0, 2],
      points: 15,
    },
    {
      id: "4",
      question: "Какие инструменты относятся к струнным?",
      questionType: "multiple",
      mediaType: "image",
      mediaUrl:
        "https://images.unsplash.com/photo-1769942788839-69f12fbd60ab?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxtdXNpY2FsJTIwaW5zdHJ1bWVudHMlMjBvcmNoZXN0cmF8ZW58MXx8fHwxNzcyNTMxNjU3fDA&ixlib=rb-4.1.0&q=80&w=1080",
      options: ["Скрипка", "Труба", "Гитара", "Барабан"],
      correctAnswers: [0, 2],
      points: 15,
    },
    {
      id: "5",
      question: "Выберите все планеты земной группы:",
      questionType: "multiple",
      options: ["Марс", "Юпитер", "Венера", "Сатурн"],
      correctAnswers: [0, 2],
      points: 15,
    },
    {
      id: "6",
      question: "В каком году началась Вторая мировая война?",
      questionType: "single",
      options: ["1937", "1939", "1941", "1945"],
      correctAnswers: [1],
      points: 10,
    },
    {
      id: "7",
      question: "Выберите произведения Льва Толстого:",
      questionType: "multiple",
      options: [
        "Война и мир",
        "Преступление и наказание",
        "Анна Каренина",
        "Мертвые души",
      ],
      correctAnswers: [0, 2],
      points: 15,
    },
    {
      id: "8",
      question: "Что вы видите на этом изображении?",
      questionType: "single",
      mediaType: "image",
      mediaUrl:
        "https://images.unsplash.com/photo-1600257729950-13a634d32697?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxuYXR1cmUlMjBsYW5kc2NhcGUlMjBtb3VudGFpbnN8ZW58MXx8fHwxNzcyNDEwMzI2fDA&ixlib=rb-4.1.0&q=80&w=1080",
      options: ["Океан", "Пустыня", "Горы", "Лес"],
      correctAnswers: [2],
      points: 10,
    },
    {
      id: "9",
      question: "Выберите языки программирования:",
      questionType: "multiple",
      options: ["Python", "HTML", "JavaScript", "CSS"],
      correctAnswers: [0, 2],
      points: 15,
    },
    {
      id: "10",
      question: "Какая самая длинная река в мире?",
      questionType: "single",
      options: ["Амазонка", "Нил", "Янцзы", "Миссисипи"],
      correctAnswers: [1],
      points: 10,
    },
  ];

  const totalQuestions = questions.length;
  const progress = ((currentQuestion + 1) / totalQuestions) * 100;
  const currentQ = questions[currentQuestion];

  // Вычисляем максимально возможный балл
  useEffect(() => {
    const maxScore = questions.reduce((sum, q) => sum + q.points, 0);
    setMaxPossibleScore(maxScore);
  }, []);

  // Таймер
  useEffect(() => {
    if (isAnswered) return;

    if (timeLeft > 0) {
      const timer = setTimeout(() => setTimeLeft(timeLeft - 1), 1000);
      return () => clearTimeout(timer);
    } else {
      // Время истекло
      handleSubmitAnswer();
    }
  }, [timeLeft, isAnswered]);

  const toggleAnswer = (index) => {
    if (isAnswered) return;

    if (currentQ.questionType === "single") {
      setSelectedAnswers([index]);
    } else {
      // Множественный выбор
      const newAnswers = [...selectedAnswers];
      const answerIndex = newAnswers.indexOf(index);
      if (answerIndex > -1) {
        newAnswers.splice(answerIndex, 1);
      } else {
        newAnswers.push(index);
      }
      setSelectedAnswers(newAnswers.sort((a, b) => a - b));
    }
  };

  const calculatePartialScore = () => {
    if (selectedAnswers.length === 0) return 0;

    const correctSet = new Set(currentQ.correctAnswers);

    // Подсчитываем правильные и неправильные выборы
    let correctSelected = 0;
    let incorrectSelected = 0;

    selectedAnswers.forEach((answer) => {
      if (correctSet.has(answer)) {
        correctSelected++;
      } else {
        incorrectSelected++;
      }
    });

    // Если есть неправильные выборы, баллы не начисляются
    if (incorrectSelected > 0) {
      return 0;
    }

    // Частичные баллы: пропорционально выбранным правильным ответам
    const percentageCorrect = correctSelected / currentQ.correctAnswers.length;
    return Math.floor(currentQ.points * percentageCorrect);
  };

  const handleSubmitAnswer = () => {
    setIsAnswered(true);

    const earnedPoints = calculatePartialScore();
    setTotalScore(totalScore + earnedPoints);

    // Считаем полностью правильный ответ
    const isFullyCorrect =
      selectedAnswers.length === currentQ.correctAnswers.length &&
      selectedAnswers.every((ans, i) => ans === currentQ.correctAnswers[i]);

    if (isFullyCorrect) {
      setCorrectCount(correctCount + 1);
    }
  };

  const handleNext = () => {
    if (currentQuestion + 1 < totalQuestions) {
      setCurrentQuestion(currentQuestion + 1);
      setSelectedAnswers([]);
      setIsAnswered(false);
      setTimeLeft(30);
    } else {
      // Квиз завершен
      setIsFinished(true);
    }
  };

  const getOptionClassName = (index) => {
    if (!isAnswered) {
      const isSelected = selectedAnswers.includes(index);
      return `answer-option ${isSelected ? "selected" : ""}`;
    }

    const isCorrect = currentQ.correctAnswers.includes(index);
    const isSelected = selectedAnswers.includes(index);

    if (isCorrect) {
      return "answer-option correct";
    }
    if (isSelected && !isCorrect) {
      return "answer-option incorrect";
    }
    return "answer-option disabled";
  };

  if (isFinished) {
    const percentScore = Math.round((totalScore / maxPossibleScore) * 100);
    navigate(`/FinishQuiz/${id}`, {
      state: {
        totalScore,
        maxPossibleScore,
        percentScore,
        correctCount,
        totalQuestions,
      },
    });

    return null;
  }

  return (
    <div className="quiz-container">
      {/* Шапка с прогрессом */}
      <div className="quiz-header">
        <div className="quiz-info">
          <div className="quiz-id">Выход</div>
          <div className="quiz-category">{currentQ.category || "Общий"}</div>
        </div>

        <div className="timer">
          <span className={`timer-value ${timeLeft <= 10 ? "warning" : ""}`}>
            {timeLeft} сек
          </span>
        </div>
      </div>

      {/* Прогресс-бар */}
      <div className="progress-container">
        <div className="progress__bar" style={{ width: `${progress}%` }}></div>
        <div className="progress__info">
          {" "}
          <div className="progress__info-text">
            Вопрос {currentQuestion + 1} из {totalQuestions}
          </div>
          <div className="progress__info-score">
            Баллы: {totalScore} / {maxPossibleScore}
          </div>
        </div>
      </div>

      {/* Счет */}

      {/* Основной контент */}
      <div className="question-container">
        {/* Медиа контент */}
        {currentQ.mediaUrl && (
          <div className="media-container">
            {currentQ.mediaType === "image" && (
              <img
                src={currentQ.mediaUrl}
                alt="Question media"
                className="media-image"
              />
            )}
            {currentQ.mediaType === "video" && (
              <video src={currentQ.mediaUrl} controls className="media-video" />
            )}
            {currentQ.mediaType === "audio" && (
              <div className="media-audio">
                <audio src={currentQ.mediaUrl} controls />
              </div>
            )}
          </div>
        )}

        <h2 className="question-title">{currentQ.question}</h2>

        <div className="question-type">
          {currentQ.questionType === "single"
            ? "Выберите один правильный ответ"
            : `Выберите все правильные ответы (${currentQ.points} баллов, частично правильный ответ дает меньше баллов)`}
        </div>

        {/* Варианты ответов */}
        <div className="answers-container">
          {currentQ.options.map((option, index) => (
            <div
              key={index}
              onClick={() => toggleAnswer(index)}
              className={getOptionClassName(index)}
            >
              {currentQ.questionType === "multiple" && !isAnswered && (
                <input
                  type="checkbox"
                  checked={selectedAnswers.includes(index)}
                  onChange={() => {}}
                  className="answer-checkbox"
                />
              )}
              <span className="answer-text">{option}</span>
              {isAnswered && currentQ.correctAnswers.includes(index) && (
                <span className="result-icon correct">✓</span>
              )}
              {isAnswered &&
                selectedAnswers.includes(index) &&
                !currentQ.correctAnswers.includes(index) && (
                  <span className="result-icon incorrect">✗</span>
                )}
            </div>
          ))}
        </div>

        {/* Результат ответа */}
        {isAnswered && (
          <div
            className={`result-message ${
              calculatePartialScore() === currentQ.points
                ? "correct"
                : calculatePartialScore() > 0
                  ? "partial"
                  : "incorrect"
            }`}
          >
            {calculatePartialScore() === currentQ.points ? (
              <p>✓ Правильно! +{currentQ.points} баллов</p>
            ) : calculatePartialScore() > 0 ? (
              <p>
                ~ Частично правильно! +{calculatePartialScore()} баллов из{" "}
                {currentQ.points}
              </p>
            ) : (
              <p>✗ Неправильно! +0 баллов</p>
            )}
          </div>
        )}
      </div>

      {/* Кнопки управления */}
      <div className="actions">
        {!isAnswered ? (
          <span
            onClick={handleSubmitAnswer}
            disabled={selectedAnswers.length === 0}
          >
            Ответить
          </span>
        ) : (
          <span onClick={handleNext}>
            {currentQuestion + 1 < totalQuestions
              ? "Следующий вопрос"
              : "Завершить квиз"}
          </span>
        )}

        <span onClick={() => handleNext()} variant="secondary">
          Пропустить вопрос
        </span>
      </div>

      {/* Таблица лидеров */}
      <div className="leaderboard-preview">
        <h3>Таблица лидеров</h3>
        <p>Места участников в данный момент</p>
        <div className="leaderboard-placeholder">
          {/* Здесь будет таблица лидеров */}
        </div>
      </div>
    </div>
  );
}
