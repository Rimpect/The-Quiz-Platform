import React from "react";
import "./Header.scss";
import { User } from "lucide-react";
import { Link } from "react-router-dom";
export function Header() {
  return (
    <header className="header__container">
      <div className="header__inner">
        <div className="header__logo">
          <div className="header__logo-icon">Q</div>
          <div className="header__logo-title">QuizMaster</div>
        </div>
        <div className="header__user">
          <User className="header__user-icon" />
          <span className="header__user-text">Имя пользователя/Гость</span>
          <Link to="/PersonalAccount" className="header__user-link">
            <button className="header__user-button">Войти</button>
          </Link>
        </div>
      </div>
    </header>
  );
}
