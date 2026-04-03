import React from "react";
import styles from "./UserAction.module.scss";
import { SmallButton } from "../../shared/Buttons/SmallButton/SmallButton";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faTools } from "@fortawesome/free-solid-svg-icons";

export function UserAction() {
  return (
    <section className={styles.section}>
      <div className={styles.filterText}>фильтры/найти квиз</div>
      <div className={styles.buttons}>
        <SmallButton>Создать квиз(кнопка)</SmallButton>

        <FontAwesomeIcon
          icon={faTools}
          size="2x"
          color="#2563eb"
          className={styles.toolsIcon}
        />

        <SmallButton>Кнопка на общую таблицу лидеров</SmallButton>
      </div>
    </section>
  );
}
