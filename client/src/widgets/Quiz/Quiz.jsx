import React from "react";
import { AverageButton } from "../../shared/Buttons/AverageButton/AverageButton";
import { useParams } from "react-router-dom";
import "./Quiz.css";
import { Link } from "react-router-dom";
export function Quiz() {
  const { id } = useParams();
  return (
    <div className="container_quiz">
      <div className="container_question">
        <div className="question">вопрос</div>
        <div className="Timer">таймер</div>
        <div>Квиз № {id}</div>
      </div>
      <div className="answer">ответ</div>
      <div>
        мб даже какая нибудь таблица лидеров для закрытого квиза? что бы типа
        отображались места в данный момент
      </div>
      <div>
        мб даже какая нибудь таблица лидеров для закрытого квиза? что бы типа
        отображались места в данный момент
      </div>

      <div className="aaaaa">
        <AverageButton>принять ответ</AverageButton>
        <Link to={`/`}>
          <AverageButton>прежде временно закончить квиз</AverageButton>
        </Link>
      </div>
    </div>
  );
}
