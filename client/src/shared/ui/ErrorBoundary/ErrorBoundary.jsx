import { Component } from 'react'

import styles from './ErrorBoundary.module.scss'

/**
 * Корневой обработчик ошибок рендера. Ловит исключения в дереве компонентов
 * (включая сбой загрузки lazy-чанка) и показывает понятный fallback вместо
 * белого экрана.
 */
export class ErrorBoundary extends Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false }
  }

  static getDerivedStateFromError() {
    return { hasError: true }
  }

  componentDidCatch(error, info) {
    // здесь можно отправлять в систему мониторинга
    console.error('Render error:', error, info)
  }

  handleReload = () => {
    window.location.reload()
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className={styles.wrapper}>
          <div className={styles.card}>
            <span className={styles.icon}>⚠️</span>
            <h2 className={styles.title}>Что-то пошло не так</h2>
            <p className={styles.text}>
              Произошла ошибка при отображении страницы. Попробуйте обновить.
            </p>
            <button className={styles.button} onClick={this.handleReload}>
              Обновить страницу
            </button>
          </div>
        </div>
      )
    }
    return this.props.children
  }
}
