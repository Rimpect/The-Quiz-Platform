import React from "react";
import { AverageButton } from "../../shared/Buttons/AverageButton/AverageButton";
import { useParams } from "react-router-dom";
import "./Quiz.css";
export function Quiz() {
  const { id } = useParams();
  return (
    <div className="container">
      <div className="Timer">таймер</div>
      <div className="question">вопрос</div>
      <div className="answer">ответ</div>
      <AverageButton>принять ответ</AverageButton>
      <div>
        мб даже какая нибудь таблица лидеров для закрытого квиза? что бы типа
        отображались места в данный момент
      </div>
      <div>Квиз № {id}</div>;
    </div>
  );
}
