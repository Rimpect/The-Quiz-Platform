import { useState } from 'react'

import { Button, ROUTES, Input } from '@shared'
import { Mail, Lock, Eye, EyeOff } from 'lucide-react'
import { useNavigate } from 'react-router-dom'

import { useLogin } from '../model/useLogin'

import styles from './LoginForm.module.scss'

export function LoginForm() {
  const [showPassword, setShowPassword] = useState(false)

  const navigate = useNavigate()
  const { login, loading } = useLogin()

  const [formData, setFormData] = useState({
    email: '',
    password: '',
  })

  const handleChange = (field, value) => {
    setFormData((prev) => ({
      ...prev,
      [field]: value,
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    const success = await login(formData)

    if (success) {
      navigate(ROUTES.main)
    }
  }

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
            <Input
              type="email"
              placeholder="your@email.com"
              value={formData.email}
              onChange={(e) => handleChange('email', e.target.value)}
              id="email"
              required
              maxLength={50}
              variant="form"
            />
          </div>

          <label htmlFor="password">Пароль</label>
          <div className={styles.relative}>
            <Lock className={styles.icon} />
            <Input
              type={showPassword ? 'text' : 'password'}
              placeholder="••••••••"
              value={formData.password}
              onChange={(e) => handleChange('password', e.target.value)}
              id="password"
              required
              variant="form"
            />
            <button
              type="button"
              className={styles.eyeButton}
              onClick={() => setShowPassword(!showPassword)}
            >
              {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
            </button>
          </div>

          <Button variant="black" size="medium" fullWidth disabled={loading}>
            {loading ? 'Загрузка...' : 'Войти'}
          </Button>
        </div>

        <div className={styles.authFooter}>
          <button
            type="button"
            className={styles.guestLink}
            onClick={() => navigate(ROUTES.main)}
          >
            Продолжить как гость
          </button>
          <div className={styles.divider}>или</div>
          <div className={styles.registerText}>
            Нет аккаунта?{' '}
            <button
              type="button"
              className={styles.registerLink}
              onClick={() => navigate(ROUTES.register)}
            >
              Зарегистрируйтесь
            </button>
          </div>
        </div>
      </form>
    </div>
  )
}
