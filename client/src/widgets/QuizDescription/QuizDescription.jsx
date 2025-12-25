import React from "react";
import "./QuizDescription.css";
import { AverageButton } from "../../shared/Buttons/AverageButton/AverageButton";
import { useParams } from "react-router-dom";
import { Link } from "react-router-dom";
export function QuizDescription() {
  const { id } = useParams();
  console.log("ID FROM PARAMS:", id);
  return (
    <div>
      <div>описание квиза Квиз № {id}</div>
      <div>описание квиза Квиз № {id}</div>
<div style={{ 
  display: 'inline-flex', 
  gap: '10px',
  flexWrap: 'wrap' /* если не помещается - перенос на новую строку */
}}>
  <Link to={`/`}>
    <AverageButton>кнопка назад</AverageButton>
  </Link>
  <Link to={`/quiz/${id}`}>
    <AverageButton>кнопка начать квиз</AverageButton>
  </Link>
</div>
    </div>
  );
}
