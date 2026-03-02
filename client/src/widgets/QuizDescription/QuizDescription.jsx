import React from "react";
import "./QuizDescription.scss";
import image1 from "../../assets/img/QuizCardTest/pic.jpg";
// import { AverageButton } from "../../shared/Buttons/AverageButton/AverageButton";
// import { useParams } from "react-router-dom";
// import { Link } from "react-router-dom";
export function QuizDescription() {
  // const { id } = useParams();
  return (
    <div className="description__inner">
      <div className="description__nav">назад к спискy</div>
      <div className="description__content">
        <div className="description__picture">
          <img src={image1} className="description__img" />
          <div className="description__overlay">11111111</div>
        </div>
        <div className="description__hero">
          <div className="description__info">
            <h2 className="description__info-title">О квизе</h2>
            <p className="description__info-text">
              Квиз о великих научных открытиях и изобретениях человечества
            </p>
            <div className="description__card">
              <h3 className="description__card-title">Что вас ждет?</h3>
              <ul className="description__card-list">
                <li className="description__card-item">
                  10 интересных вопросов
                </li>
                <li className="description__card-item">
                  Ограничение по времени на каждый вопрос
                </li>
                <li className="description__card-item">
                  Мгновенная проверка ответов
                </li>
                <li className="description__card-item">
                  Подробная статистика в конце
                </li>
              </ul>
            </div>
          </div>
          <div className="description__stats">
            <ul className="description__stats-list">
              <li className="description__stats-item">
                {" "}
                <span className="stats-item__icon">иконка</span>
                <span className="stats-item__label">Участников:</span>
                <span className="stats-item__value">128</span>
              </li>
              <li className="description__stats-item">
                {" "}
                <span className="stats-item__icon">иконка</span>
                <span className="stats-item__label">Длительность:</span>
                <span className="stats-item__value">10 минут</span>
              </li>
              <li className="description__stats-item">
                {" "}
                <span className="stats-item__icon">иконка</span>
                <span className="stats-item__label">Лучший результат:</span>
                <span className="stats-item__value">100%</span>
              </li>
              <li className="description__stats-item">
                {" "}
                <span className="stats-item__icon">иконка</span>
                <span className="stats-item__label">Вопросов:</span>
                <span className="stats-item__value">10</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
//  <div>описание квиза Квиз № {id}</div>
//       <div
//         style={{
//           display: "inline-flex",
//           gap: "10px",
//           flexWrap: "wrap" /* если не помещается - перенос на новую строку */,
//         }}
//       >
//         <Link to={`/`}>
//           <AverageButton>кнопка назад</AverageButton>
//         </Link>
//         <Link to={`/quiz/${id}`}>
//           <AverageButton>кнопка начать квиз</AverageButton>
//         </Link>
//       </div>
