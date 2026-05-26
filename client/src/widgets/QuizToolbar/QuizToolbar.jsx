import React, { useState } from 'react'
import { Button, SearchBar, ModalFilter } from '@shared'
import { SlidersHorizontal } from 'lucide-react'

import styles from './QuizToolbar.module.scss'

export function QuizToolbar() {
  const [isFilterOpen, setIsFilterOpen] = useState(false)
  // const [searchQuery, setSearchQuery] = useState('')

  // Заглушка для обработки поиска
  // const handleSearch = (e) => {
  //   setSearchQuery(e.target.value)
  //   console.log('Поиск:', e.target.value)
  // }

  // Открытие фильтров
  const handleFilterClick = () => {
    setIsFilterOpen(true)
    console.log('Открыть фильтры')
  }

  // Закрытие фильтров
  const handleFilterClose = () => {
    setIsFilterOpen(false)
    console.log('Закрыть фильтры')
  }

  // Применение фильтров
  const handleApplyFilters = (filters) => {
    console.log('Примененные фильтры:', filters)
    // Здесь будет логика применения фильтров
    setIsFilterOpen(false)
  }

  return (
    <>
      <div className={styles.quizSearch}>
        <div className={styles.container}>
          <div className={styles.searchRow}>
            <Button
              variant="white"
              className={styles.filterButton}
              onClick={handleFilterClick}
              aria-label="Открыть фильтры"
              icon={<SlidersHorizontal size={18} />}
            />

            <SearchBar elevated={false} />
            {/* @TODO переделать поиск */}
          </div>
        </div>
      </div>
      <ModalFilter
        isOpen={isFilterOpen}
        onClose={handleFilterClose}
        onApply={handleApplyFilters}
      />
    </>
  )
}
