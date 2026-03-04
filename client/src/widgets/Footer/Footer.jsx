import React from "react";
import "./Footer.scss";
import { Mail, Phone, MapPin } from "lucide-react";
export function Footer() {
  return (
    <footer className="footer__container">
      <div class="footer__inner">
        <div className="footer__description">
          <p className="footer__description-header">О QuizMaster</p>
          <p className="footer__description-title">
            Платформа для проведения <br />
            интеллектуальных квизов. Проверьте свои <br />
            знания и соревнуйтесь с друзьями!
          </p>
        </div>
        <div className="footer__menu">
          <ul className="footer__list">
            <li className="footer__list-item">Поддержка</li>
            <li className="footer__list-item">Помощь</li>
            <li className="footer__list-item">FAQ</li>
            <li className="footer__list-item">Правила</li>
          </ul>

          <ul className="footer__list">
            <li className="footer__list-item">Контакты</li>
            <li className="footer__list-item">
              <Mail className="footer__list-icon" />
              info@quizmaster.ru
            </li>
            <li className="footer__list-item">
              {" "}
              <Phone className="footer__list-icon" />
              +7 (495) 123-45-67
            </li>
            <li className="footer__list-item">
              {" "}
              <MapPin className="footer__list-icon" />
              Россия
            </li>
          </ul>
        </div>
      </div>
      <div className="footer__copyright">
        <p>&copy; 2026 QuizMaster. Все права защищены.</p>
      </div>
    </footer>
  );
}
