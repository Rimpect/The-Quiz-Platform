import React from 'react'
import { Link } from 'react-router-dom'
import styles from './NotFoundPage.module.scss'

export function NotFoundPage() {
  return (
    <div className={styles.container}>
      <h1 className={styles.message}>Ошибка 404</h1>
      <div className={styles.info}>
        Кажется что-то пошло не так! Страница которую вы запрашиваете, не
        <br></br>
        существует. Возможно она была удалена, или вы набрали неверный адрес.
        <br></br>
        Передите на нашу{' '}
        <Link to="/MainPage" className={styles.link}>
          главную страницу
        </Link>{' '}
        и попробуйте найти необходимую <br></br>
        информацию там
      </div>
    </div>
  )
}
