import React from "react";
import "./UserAction.scss";
import { SmallButton } from "../../shared/Buttons/SmallButton/SmallButton";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faTools } from "@fortawesome/free-solid-svg-icons";
export function UserAction() {
  return (
    <section>
      <div>фильтры/найти квиз</div>
      <div className="buttons">
        <SmallButton>Создать квиз(кнопка)</SmallButton>
        <FontAwesomeIcon
          icon={faTools}
          size="10x" // xs, sm, lg, 2x, 3x, 4x, 5x, 6x, 7x, 8x, 9x, 10x
          color="green" // любой CSS цвет
          spin // анимация вращения
          pulse // пульсирующая анимация
          rotation={90} // поворот на 90 градусов
          flip="horizontal" // horizontal, vertical, both
          transform="shrink-6 left-4" // трансформации
          style={{ marginRight: "10px" }} // инлайн стили
          className="my-custom-class" // CSS класс
        />
        <SmallButton>Кнопка на общую таблицу лидеров</SmallButton>
      </div>
    </section>
  );
}
