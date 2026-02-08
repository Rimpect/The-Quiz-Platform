import React from "react";
import "./Header.scss";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faUser } from "@fortawesome/free-solid-svg-icons";
import { Link } from "react-router-dom";
export function Header() {
  return (
    <header className="header">
      <div className="header__inner">
        <div className="header__logo">Quizus</div>
        <div className="header__user">
          <Link to="/PersonalAccount" className="header__user-link">
            <FontAwesomeIcon icon={faUser} className="header__user-icon" />
            <span className="header__user-text">Имя пользователя/Гость</span>
          </Link>
        </div>
      </div>
    </header>
  );
}
