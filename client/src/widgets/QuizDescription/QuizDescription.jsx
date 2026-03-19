import React from "react";
import "./QuizDescription.scss";
import image1 from "../../assets/img/QuizCardTest/pic.jpg";
import { ArrowLeft, Users, Clock, Trophy, Star, Award } from "lucide-react";
import { Link } from "react-router-dom";
export function QuizDescription() {
  // Заглушки данных
  const quizData = {
    id: 1,
    title: "Великие научные открытия",
    description: "Квиз о великих научных открытиях и изобретениях человечества",
    category: "Наука",
    difficulty: "Средний",
    rating: 4.7,
    participants: 1234,
    duration: 45,
    topScore: 98,
    questionCount: 20,
    image: image1,
  };

  // Цвета для сложности
  const difficultyColor = {
    Легкий: "description__badge--easy",
    Средний: "description__badge--medium",
    Сложный: "description__badge--hard",
  };

  return (
    <div className="description">
      <div className="description__container">
        {/* Навигация */}

        <Link to={`/`} className="description__nav">
          <ArrowLeft className="description__nav-icon" />
          <span>Назад к списку</span>
        </Link>

        {/* Основной контент */}
        <div className="description__content">
          {/* Картинка с оверлеем */}
          <div className="description__picture">
            <img
              src={quizData.image}
              alt={quizData.title}
              className="description__img"
            />
            <div className="description__overlay">
              <div className="description__overlay-content">
                <div className="description__meta">
                  <Trophy className="description__meta-icon" />
                  <span className="description__meta-category">
                    {quizData.category}
                  </span>
                  <span
                    className={`description__badge ${difficultyColor[quizData.difficulty]}`}
                  >
                    {quizData.difficulty}
                  </span>
                </div>
                <h1 className="description__title">{quizData.title}</h1>
                <div className="description__rating">
                  <Star className="description__rating-icon" />
                  <span className="description__rating-value">
                    {quizData.rating}
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Две колонки */}
          <div className="description__columns">
            {/* Левая колонка - описание */}
            <div className="description__info">
              <h2 className="description__info-title">О квизе</h2>
              <p className="description__info-text">{quizData.description}</p>

              <div className="description__card">
                <h3 className="description__card-title">Что вас ждет?</h3>
                <ul className="description__card-list">
                  <li className="description__card-item">
                    • {quizData.questionCount} интересных вопросов
                  </li>
                  <li className="description__card-item">
                    • Ограничение по времени на каждый вопрос
                  </li>
                  <li className="description__card-item">
                    • Мгновенная проверка ответов
                  </li>
                  <li className="description__card-item">
                    • Подробная статистика в конце
                  </li>
                </ul>
              </div>
            </div>

            {/* Правая колонка - статистика и кнопка */}
            <div className="description__stats-wrapper">
              <h2 className="description__stats-title">Статистика</h2>

              <ul className="description__stats-list">
                <li className="description__stats-item">
                  <div className="description__stats-left">
                    <span className="description__stats-icon">
                      <Users />
                    </span>
                    <span className="description__stats-label">
                      Участников:
                    </span>
                  </div>
                  <span className="description__stats-value">
                    {quizData.participants.toLocaleString()}
                  </span>
                </li>

                <li className="description__stats-item">
                  <div className="description__stats-left">
                    <span className="description__stats-icon">
                      <Clock />
                    </span>
                    <span className="description__stats-label">
                      Длительность:
                    </span>
                  </div>
                  <span className="description__stats-value">
                    {quizData.duration} минут
                  </span>
                </li>

                <li className="description__stats-item">
                  <div className="description__stats-left">
                    <span className="description__stats-icon">
                      <Award />
                    </span>
                    <span className="description__stats-label">
                      Лучший результат:
                    </span>
                  </div>
                  <span className="description__stats-value">
                    {quizData.topScore}%
                  </span>
                </li>

                <li className="description__stats-item">
                  <div className="description__stats-left">
                    <span className="description__stats-icon">
                      <Trophy />
                    </span>
                    <span className="description__stats-label">Вопросов:</span>
                  </div>
                  <span className="description__stats-value">
                    {quizData.questionCount}
                  </span>
                </li>
              </ul>

              <Link to={`/QuizPage/:id`} className="description__start-btn">
                <span>Начать квиз</span>
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
