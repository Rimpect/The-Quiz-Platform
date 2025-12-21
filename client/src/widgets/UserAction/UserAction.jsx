import React from "react";
import "./UserAction.css";
import { SmallButton } from "../../shared/Buttons/SmallButton/SmallButton";
export function UserAction() {
  return (
    <section>
      <div>фильтры/найти квиз</div>
      <div className="buttons">
        <SmallButton>Создать квиз(кнопка)</SmallButton>
        
        <SmallButton>Кнопка на общую таблицу лидеров</SmallButton>
      </div>
    </section>
  );
}
