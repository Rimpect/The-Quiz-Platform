import React from "react";
import "./QuizDescription.scss";
// import { AverageButton } from "../../shared/Buttons/AverageButton/AverageButton";
// import { useParams } from "react-router-dom";
// import { Link } from "react-router-dom";
export function QuizDescription() {
  // const { id } = useParams();
  return (
    <div className="description__inner">
      <div className="description__nav">111</div>
      <div className="description__img">123</div>
      <div className="description__content">
        <div className="description__info">
          <h2 className="description__info-title">О квизе</h2>
          <p className="description__info-text">
            Квиз о великих научных открытиях и изобретениях человечества
          </p>
          <div className="description__card">
            <ul className="description__card-list">
              <li className="description__card-item">10 интересных вопросов</li>
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
            <li className="description__stats-item">Участников:</li>
            <li className="description__stats-item">Длительность:</li>
            <li className="description__stats-item">Лучший результат:</li>
            <li className="description__stats-item">Вопросов:</li>
          </ul>
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
