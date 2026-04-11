import React, { useState } from "react";
import styles from "./SignUp.module.scss";
import { Mail, Lock, Eye, EyeOff } from "lucide-react";
import { useNavigate } from "react-router-dom";

export function SignUp() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Login:", { email, password });
  };

  return (
    <div className={styles.page}>
      <form className={styles.container} onSubmit={handleSubmit}>
        <div className={styles.authGreeting}>
          <div className={styles.logo}>Q</div>
          <div className={styles.welcomeText}>Добро пожаловать!</div>
          <div className={styles.subtitle}>
            Войдите в свой аккаунт QuizMaster
          </div>
        </div>

        <div className={styles.authAction}>
          <label htmlFor="email">Email</label>
          <div className={styles.relative}>
            <Mail className={styles.icon} />
            <input
              type="email"
              placeholder="your@email.com"
              name="email"
              id="email"
              required
              className={styles.input}
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>

          <label htmlFor="password">Пароль</label>
          <div className={styles.relative}>
            <Lock className={styles.icon} />
            <input
              type={showPassword ? "text" : "password"}
              placeholder="••••••••"
              name="password"
              id="password"
              required
              className={styles.input}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <button
              type="button"
              className={styles.eyeButton}
              onClick={() => setShowPassword(!showPassword)}
            >
              {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
            </button>
          </div>

          <button type="submit" className={styles.submitButton}>
            Войти
          </button>
        </div>

        <div className={styles.authFooter}>
          <button
            type="button"
            className={styles.guestLink}
            onClick={() => navigate("/MainPage")}
          >
            Продолжить как гость
          </button>
          <div className={styles.divider}>или</div>
          <div className={styles.registerText}>
            Нет аккаунта?{" "}
            <button
              type="button"
              className={styles.registerLink}
              onClick={() => navigate("/RegistrationPage")}
            >
              Зарегистрируйтесь 
            </button>
          </div>
        </div>
      </form>
    </div>
  );
}
