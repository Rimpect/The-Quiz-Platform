import React, { useState } from 'react'

import { Link } from 'react-router-dom'

import { SmallButton } from '../../shared/Buttons/SmallButton/SmallButton'
import { ModalNotifications } from '../../shared/Modal/ModalNotifications/ModalNotifications'
import { QuizCard } from '../../shared/QuizCard/QuizCard/QuizCard'

import styles from './QuizeBoard.module.scss'

export function QuizeBoard() {
  const [open, setOpen] = useState(false)

  const quizzes = [
    {
      id: 1,
      img: '/img/QuizCardTest/1.webp',
      title: 'Основы JavaScript',
      description:
        'Проверьте свои знания основ JavaScript: переменные, функции, циклы и основы ООП',
      difficulty: 'Легкий',
      category: 'Программирование',
      participants: '1.2K',
      duration: 15,
    },
    {
      id: 2,
      img: '/img/QuizCardTest/i2.webp',
      title: 'Путешествия по Европе',
      description:
        'Угадайте страну по достопримечательности и проверьте свои знания географии',
      difficulty: 'Средний',
      category: 'География',
      participants: '856',
      duration: 20,
    },
    {
      id: 3,
      img: '/img/QuizCardTest/1.webp',
      title: 'История Древнего мира',
      description:
        'От Египта до Рима: проверьте, что вы помните из школьной программы',
      difficulty: 'Сложный',
      category: 'История',
      participants: '2.1K',
      duration: 25,
    },
    {
      id: 4,
      img: '/img/QuizCardTest/i2.webp',
      title: 'Кино 90-х',
      description:
        'Лучшие фильмы десятилетия: цитаты, актеры и культовые сцены',
      difficulty: 'Средний',
      category: 'Кино',
      participants: '3.4K',
      duration: 15,
    },
    {
      id: 5,
      img: '/img/QuizCardTest/1.webp',
      title: 'React для начинающих',
      description: 'Хуки, компоненты, состояние и жизненный цикл в React',
      difficulty: 'Средний',
      category: 'Программирование',
      participants: '954',
      duration: 20,
    },
    {
      id: 6,
      img: '/img/QuizCardTest/i2.webp',
      title: 'Рок-музыка',
      description: 'От Led Zeppelin до Nirvana: угадайте группу по песне',
      difficulty: 'Сложный',
      category: 'Музыка',
      participants: '1.8K',
      duration: 20,
    },
    {
      id: 7,
      img: '/img/QuizCardTest/1.webp',
      title: 'Космос и астрономия',
      description:
        'Планеты, звезды и галактики: насколько хорошо вы знаете Вселенную?',
      difficulty: 'Средний',
      category: 'Наука',
      participants: '2.3K',
      duration: 25,
    },
    {
      id: 8,
      img: '/img/QuizCardTest/i2.webp',
      title: 'Литература XIX века',
      description: 'Русская и зарубежная классика: авторы, герои и сюжеты',
      difficulty: 'Сложный',
      category: 'Литература',
      participants: '647',
      duration: 30,
    },
    {
      id: 9,
      img: '/img/QuizCardTest/1.webp',
      title: 'Спортивные рекорды',
      description: 'Олимпийские игры, чемпионаты мира и легендарные спортсмены',
      difficulty: 'Легкий',
      category: 'Спорт',
      participants: '1.5K',
      duration: 15,
    },
    {
      id: 10,
      img: '/img/QuizCardTest/i2.webp',
      title: 'Кулинария мира',
      description: 'Национальные блюда, ингредиенты и кулинарные традиции',
      difficulty: 'Средний',
      category: 'Еда',
      participants: '2.7K',
      duration: 20,
    },
    {
      id: 11,
      img: '/img/QuizCardTest/1.webp',
      title: 'Технологии будущего',
      description:
        'ИИ, роботы, нейросети и другие технологии, которые меняют мир',
      difficulty: 'Средний',
      category: 'Технологии',
      participants: '3.1K',
      duration: 25,
    },
    {
      id: 12,
      img: '/img/QuizCardTest/i2.webp',
      title: 'Животный мир',
      description: 'Удивительные факты о животных со всего света',
      difficulty: 'Легкий',
      category: 'Природа',
      participants: '4.2K',
      duration: 15,
    },
  ]

  return (
    <div className={styles.containerBoard}>
      <div className={styles.dashboardQuiz}>
        {quizzes.map((quiz) => (
          <Link key={quiz.id} to={`/QuizDescription/${quiz.id}`}>
            <QuizCard {...quiz} />
          </Link>
        ))}

        {open && (
          <ModalNotifications open={open} onClose={() => setOpen(false)}>
            буковки
          </ModalNotifications>
        )}
      </div>
      <div className={styles.nav}>
        <SmallButton>Кнопка вперед</SmallButton>
        <div>выбрать страницу</div>
        <SmallButton>Кнопка Назад</SmallButton>
      </div>
    </div>
  )
}
