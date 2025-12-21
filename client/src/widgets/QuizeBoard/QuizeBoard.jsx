import React from "react";
import "./QuizeBoard.css";
import { SmallButton } from "../../shared/Buttons/SmallButton/SmallButton";
import { QuizButton } from "../../shared/Buttons/QuizButton/QuizButton";
export function QuizeBoard() {
  return (
    <div>
      <div className="container">
        <QuizButton>
          <img src="/img/QuizCardTest/1.webp" />
        </QuizButton>
        <QuizButton>
          {" "}
          <img src="/img/QuizCardTest/i2.webp" />
        </QuizButton>
        <QuizButton>
          <img src="/img/QuizCardTest/1.webp" />
        </QuizButton>
        <QuizButton>
          {" "}
          <img src="/img/QuizCardTest/i2.webp" />
        </QuizButton>
        <QuizButton>
          <img src="/img/QuizCardTest/1.webp" />
        </QuizButton>
        <QuizButton>
          {" "}
          <img src="/img/QuizCardTest/i2.webp" />
        </QuizButton>
        <QuizButton>
          <img src="/img/QuizCardTest/1.webp" />
        </QuizButton>
        <QuizButton>
          {" "}
          <img src="/img/QuizCardTest/i2.webp" />
        </QuizButton>
        <QuizButton>
          <img src="/img/QuizCardTest/1.webp" />
        </QuizButton>
        <QuizButton>
          {" "}
          <img src="/img/QuizCardTest/i2.webp" />
        </QuizButton>
        <QuizButton>
          <img src="/img/QuizCardTest/1.webp" />
        </QuizButton>
        <QuizButton>
          {" "}
          <img src="/img/QuizCardTest/i2.webp" />
        </QuizButton>
      </div>
      <div className="nav">
        <SmallButton>Кнопка вперед</SmallButton>
        <div>выбрать страницу</div>
        <SmallButton>Кнопка Назад</SmallButton>
      </div>
    </div>
  );
}
