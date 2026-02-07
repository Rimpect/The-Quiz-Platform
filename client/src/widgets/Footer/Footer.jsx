import React from "react";
import "./Footer.scss";
export function Footer() {
  return (
    <footer className="footer container">
      <div className="footer__inner">
        <div className="footer__navigation">
          <p className="visually-hidden">Подвал</p>
          {/* для скрин ридера */}
          <a class="footer__logo logo" href="/">
            <img
              class="logo__image"
              src=""
              alt="Logo"
              width="180"
              height="29"
              loading="lazy"
            />
          </a>
          <div className="footer__menu">
            <li className="footer__list">
              <ul className="footer__item">1</ul>
              <ul className="footer__item">2</ul>
              <ul className="footer__item">3</ul>
            </li>
          </div>
        </div>
      </div>
    </footer>
  );
}
