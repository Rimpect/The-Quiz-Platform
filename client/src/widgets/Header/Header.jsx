import React from "react";
import "./Header.scss";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faUser } from "@fortawesome/free-solid-svg-icons";
import { Link } from "react-router-dom";
export function Header() {
  return (
    <header className='header'>
 
      <div className="header__logo">Logo</div>
      <div className="header__UserName">
        <Link to="/PersonalAccount">
          {" "}
          <FontAwesomeIcon icon={faUser} />
        </Link>
        Имя пользователя/Гость
      </div>
      
    </header>
  );
}
