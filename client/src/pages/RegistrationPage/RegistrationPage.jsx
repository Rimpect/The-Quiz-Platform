import React, { useState } from "react";
import styles from "./RegistrationPage.module.scss";
import { Mail, User, Lock, Eye, EyeOff } from "lucide-react";
import { useNavigate } from "react-router-dom";

export default function RegistrationPage() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    //@TODO сделать потом toast уведомления
    if (!name.trim()) {
      alert("Введите ваше имя");
      return;
    }

    if (!email.trim()) {
      alert("Введите email");
      return;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      alert("Введите корректный email");
      return;
    }

    if (!password) {
      alert("Введите пароль");
      return;
    }

    if (password.length < 6) {
      alert("Пароль должен содержать минимум 6 символов");
      return;
    }

    if (password !== confirmPassword) {
      alert("Пароли не совпадают");
      return;
    }
    console.log("Register:", { name, email, password });
    navigate("/MainPage");
  };

  return (
    <div className={styles.page}>
      <form className={styles.container} onSubmit={handleSubmit}>
        <div className={styles.authGreeting}>
          <div className={styles.logo}>Q</div>
          <div className={styles.welcomeText}>Создать аккаунт</div>
          <div className={styles.subtitle}>Присоединяйтесь к QuizMaster</div>
        </div>

        <div className={styles.authAction}>
          <label htmlFor="name">Имя</label>
          <div className={styles.relative}>
            <User className={styles.icon} />
            <input
              type="text"
              placeholder="Ваше имя"
              name="name"
              id="name"
              required
              className={styles.input}
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
          </div>

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

          <label htmlFor="confirmPassword">Подтвердите пароль</label>
          <div className={styles.relative}>
            <Lock className={styles.icon} />
            <input
              type={showConfirmPassword ? "text" : "password"}
              placeholder="••••••••"
              name="confirmPassword"
              id="confirmPassword"
              required
              className={styles.input}
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
            />
            <button
              type="button"
              className={styles.eyeButton}
              onClick={() => setShowConfirmPassword(!showConfirmPassword)}
            >
              {showConfirmPassword ? <EyeOff size={18} /> : <Eye size={18} />}
            </button>
          </div>

          <button type="submit" className={styles.submitButton}>
            Зарегистрироваться
          </button>
        </div>
      </form>
    </div>
  );
}
