import React, { useState } from 'react'

import { useCategories } from '@entities'
import { useSearchStore } from '@features'
import { Button, SearchBar, ModalFilter } from '@shared'
import { SlidersHorizontal } from 'lucide-react'

import styles from './QuizToolbar.module.scss'

export function QuizToolbar() {
  const [isFilterOpen, setIsFilterOpen] = useState(false)
  const { categories } = useCategories()
  const query = useSearchStore((state) => state.query)
  const filter = useSearchStore((state) => state.filter)
  const setQuery = useSearchStore((state) => state.setQuery)
  const setFilter = useSearchStore((state) => state.setFilter)
  const resetFilters = useSearchStore((state) => state.resetFilters)

  const handleFilterClick = () => {
    setIsFilterOpen(true)
  }

  const handleFilterClose = () => {
    setIsFilterOpen(false)
  }

  const handleApplyFilters = (filters) => {
    setFilter(filters)
    setIsFilterOpen(false)
  }

  const handleResetFilters = () => {
    resetFilters()
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

            <SearchBar
              elevated={false}
              value={query}
              onChange={setQuery}
              placeholder="Поиск по названию или автору..."
            />
          </div>
        </div>
      </div>
      <ModalFilter
        isOpen={isFilterOpen}
        onClose={handleFilterClose}
        onApply={handleApplyFilters}
        onReset={handleResetFilters}
        filter={filter}
        categories={categories}
      />
    </>
  )
}
