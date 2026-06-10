import { useState } from 'react'

import { Button, ROUTES, Input } from '@shared'
import { Mail, User, Lock, Eye, EyeOff } from 'lucide-react'
import { useNavigate } from 'react-router-dom'

import { useRegister } from '../model/useRegister'

import styles from './RegistrationForm.module.scss'

export function RegistrationForm() {
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)

  const navigate = useNavigate()

  const { register, loading } = useRegister()

  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
  })

  const handleChange = (field, value) => {
    setFormData((prev) => ({
      ...prev,
      [field]: value,
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    const success = await register(formData)

    if (success) {
      navigate(ROUTES.main)
    }
  }
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
            <Input
              type="text"
              placeholder="Имя"
              value={formData.name}
              onChange={(e) => handleChange('name', e.target.value)}
              id="name"
              required
              maxLength={50}
              className={styles.input}
            />
          </div>

          <label htmlFor="email">Email</label>
          <div className={styles.relative}>
            <Mail className={styles.icon} />
            <Input
              type="email"
              placeholder="Email"
              value={formData.email}
              onChange={(e) => handleChange('email', e.target.value)}
              id="email"
              required
              maxLength={50}
              className={styles.input}
            />
          </div>

          <label htmlFor="password">Пароль</label>
          <div className={styles.relative}>
            <Lock className={styles.icon} />
            <Input
              type={showPassword ? 'text' : 'password'}
              placeholder="••••••••"
              name="password"
              id="password"
              required
              className={styles.input}
              value={formData.password}
              onChange={(e) => handleChange('password', e.target.value)}
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
            <Input
              type={showConfirmPassword ? 'text' : 'password'}
              placeholder="••••••••"
              value={formData.confirmPassword}
              id="confirmPassword"
              required
              className={styles.input}
              onChange={(e) => handleChange('confirmPassword', e.target.value)}
            />
            <button
              type="button"
              className={styles.eyeButton}
              onClick={() => setShowConfirmPassword(!showConfirmPassword)}
            >
              {showConfirmPassword ? <EyeOff size={18} /> : <Eye size={18} />}
            </button>
          </div>
          <Button variant="black" size="medium" fullWidth disabled={loading}>
            {loading ? 'Загрузка...' : 'Регистрация'}
          </Button>
        </div>
      </form>
    </div>
  )
}
