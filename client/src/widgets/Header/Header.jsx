import React from "react";
import styles from "./Header.module.scss";
import { User } from "lucide-react";
import { Link } from "react-router-dom";

export function Header() {
  return (
    <header className={styles.headerContainer}>
      <div className={styles.headerInner}>
        <div className={styles.logo}>
          <div className={styles.logoIcon}>Q</div>
          <div className={styles.logoTitle}>QuizMaster</div>
        </div>
        <div className={styles.user}>
          <User className={styles.userIcon} />
          <span className={styles.userText}>Имя пользователя/Гость</span>
          <Link to="/PersonalAccount" className={styles.userLink}>
            <button className={styles.userButton}>Войти</button>
          </Link>
        </div>
      </div>
    </header>
  );
}
