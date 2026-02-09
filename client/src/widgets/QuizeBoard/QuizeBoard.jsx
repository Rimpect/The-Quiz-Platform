import React from "react";
import "./QuizeBoard.scss";
import { SmallButton } from "../../shared/Buttons/SmallButton/SmallButton";
import { useState } from "react";
import { ModalNotifications } from "../../shared/Modal/ModalNotifications/ModalNotifications";
import { Link } from "react-router-dom";
import { QuizCard } from "../../shared/QuizCard/QuizCard/QuizCard";
export function QuizeBoard() {
  const [open, setOpen] = useState(false);
  const quizzes = [
    { id: 1, img: "/img/QuizCardTest/1.webp" },
    { id: 2, img: "/img/QuizCardTest/i2.webp" },
    { id: 3, img: "/img/QuizCardTest/1.webp" },
    { id: 4, img: "/img/QuizCardTest/i2.webp" },
    { id: 5, img: "/img/QuizCardTest/1.webp" },
    { id: 6, img: "/img/QuizCardTest/i2.webp" },
    { id: 7, img: "/img/QuizCardTest/1.webp" },
    { id: 8, img: "/img/QuizCardTest/i2.webp" },
    { id: 9, img: "/img/QuizCardTest/1.webp" },
    { id: 10, img: "/img/QuizCardTest/i2.webp" },
    { id: 11, img: "/img/QuizCardTest/1.webp" },
    { id: 12, img: "/img/QuizCardTest/i2.webp" },
  ];

  return (
    <section className="dashboardQuiz">
      <div className="containerBoard">
        {quizzes.map((quiz) => (
          <Link key={quiz.id} to={`/QuizDescription/${quiz.id}`}>
            <QuizCard img={quiz.img} id={quiz.id} />
          </Link>
        ))}
        {/* <QuizButton onClick={() => setOpen(true)}>
          <img src="/img/QuizCardTest/1.webp" alt="quiz" />
        </QuizButton> */}
        {/* ------------------ работа модалок */}
        {open && (
          <ModalNotifications open={open} onClose={() => setOpen(false)}>
            буковки
          </ModalNotifications>
        )}
      </div>
      <div className="nav">
        <SmallButton>Кнопка вперед</SmallButton>
        <div>выбрать страницу</div>
        <SmallButton>Кнопка Назад</SmallButton>
      </div>
    </section>
  );
}
