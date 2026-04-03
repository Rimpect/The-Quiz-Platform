import React from "react";
import styles from "./QuizDescription.module.scss";
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

  return (
    <div className={styles.description}>
      <div className={styles.container}>
        {/* Навигация */}
        <Link to={`/`} className={styles.nav}>
          <ArrowLeft className={styles.navIcon} />
          <span>Назад к списку</span>
        </Link>

        {/* Основной контент */}
        <div className={styles.content}>
          {/* Картинка с оверлеем */}
          <div className={styles.picture}>
            <img
              src={quizData.image}
              alt={quizData.title}
              className={styles.img}
            />
            <div className={styles.overlay}>
              <div className={styles.overlayContent}>
                <div className={styles.meta}>
                  <Trophy className={styles.metaIcon} />
                  <span className={styles.metaCategory}>
                    {quizData.category}
                  </span>
                  <span
                    className={`${styles.badge} ${
                      (quizData.difficulty === "Легкий" && styles.easy) ||
                      (quizData.difficulty === "Средний" && styles.medium) ||
                      (quizData.difficulty === "Сложный" && styles.hard)
                    }`}
                  >
                    {quizData.difficulty}
                  </span>
                </div>
                <h1 className={styles.title}>{quizData.title}</h1>
                <div className={styles.rating}>
                  <Star className={styles.ratingIcon} />
                  <span className={styles.ratingValue}>{quizData.rating}</span>
                </div>
              </div>
            </div>
          </div>

          {/* Две колонки */}
          <div className={styles.columns}>
            {/* Левая колонка - описание */}
            <div>
              <h2 className={styles.infoTitle}>О квизе</h2>
              <p className={styles.infoText}>{quizData.description}</p>

              <div className={styles.card}>
                <h3 className={styles.cardTitle}>Что вас ждет?</h3>
                <ul className={styles.cardList}>
                  <li className={styles.cardItem}>
                    • {quizData.questionCount} интересных вопросов
                  </li>
                  <li className={styles.cardItem}>
                    • Ограничение по времени на каждый вопрос
                  </li>
                  <li className={styles.cardItem}>
                    • Мгновенная проверка ответов
                  </li>
                  <li className={styles.cardItem}>
                    • Подробная статистика в конце
                  </li>
                </ul>
              </div>
            </div>

            {/* Правая колонка - статистика и кнопка */}
            <div>
              <h2 className={styles.statsTitle}>Статистика</h2>

              <ul className={styles.statsList}>
                <li className={styles.statsItem}>
                  <div className={styles.statsLeft}>
                    <span className={styles.statsIcon}>
                      <Users />
                    </span>
                    <span className={styles.statsLabel}>Участников:</span>
                  </div>
                  <span className={styles.statsValue}>
                    {quizData.participants.toLocaleString()}
                  </span>
                </li>

                <li className={styles.statsItem}>
                  <div className={styles.statsLeft}>
                    <span className={styles.statsIcon}>
                      <Clock />
                    </span>
                    <span className={styles.statsLabel}>Длительность:</span>
                  </div>
                  <span className={styles.statsValue}>
                    {quizData.duration} минут
                  </span>
                </li>

                <li className={styles.statsItem}>
                  <div className={styles.statsLeft}>
                    <span className={styles.statsIcon}>
                      <Award />
                    </span>
                    <span className={styles.statsLabel}>Лучший результат:</span>
                  </div>
                  <span className={styles.statsValue}>
                    {quizData.topScore}%
                  </span>
                </li>

                <li className={styles.statsItem}>
                  <div className={styles.statsLeft}>
                    <span className={styles.statsIcon}>
                      <Trophy />
                    </span>
                    <span className={styles.statsLabel}>Вопросов:</span>
                  </div>
                  <span className={styles.statsValue}>
                    {quizData.questionCount}
                  </span>
                </li>
              </ul>

              <Link to={`/QuizPage/:id`} className={styles.startBtn}>
                <span>Начать квиз</span>
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
