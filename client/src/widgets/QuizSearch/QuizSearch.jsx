import React, { useState } from "react";
import { SlidersHorizontal, Search } from "lucide-react";
import styles from "./QuizSearch.module.scss";
import ModalFilter from "../../shared/Modal/ModalFilter/ModalFilter";

export function QuizSearch() {
  const [isFilterOpen, setIsFilterOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");

  // Заглушка для обработки поиска
  const handleSearch = (e) => {
    setSearchQuery(e.target.value);
    console.log("Поиск:", e.target.value);
  };

  // Открытие фильтров
  const handleFilterClick = () => {
    setIsFilterOpen(true);
    console.log("Открыть фильтры");
  };

  // Закрытие фильтров
  const handleFilterClose = () => {
    setIsFilterOpen(false);
    console.log("Закрыть фильтры");
  };

  // Применение фильтров
  const handleApplyFilters = (filters) => {
    console.log("Примененные фильтры:", filters);
    // Здесь будет логика применения фильтров
    setIsFilterOpen(false);
  };

  return (
    <>
      <div className={styles.quizSearch}>
        <div className={styles.container}>
          <div className={styles.wrapper}>
            <button
              className={styles.filterBtn}
              onClick={handleFilterClick}
              aria-label="Открыть фильтры"
            >
              <SlidersHorizontal className={styles.filterIcon} />
            </button>

            <div className={styles.inputWrapper}>
              <Search className={styles.searchIcon} />
              <input
                type="text"
                className={styles.input}
                placeholder="Поиск квизов..."
                value={searchQuery}
                onChange={handleSearch}
              />
            </div>
          </div>
        </div>
      </div>
      <ModalFilter
        isOpen={isFilterOpen}
        onClose={handleFilterClose}
        onApply={handleApplyFilters}
      />
    </>
  );
}
