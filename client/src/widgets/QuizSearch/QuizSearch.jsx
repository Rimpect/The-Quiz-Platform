import React, { useState } from "react";
import { SlidersHorizontal, Search } from "lucide-react";
import "./QuizSearch.scss";

export function QuizSearch() {
  const [isFilterOpen, setIsFilterOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");

  // Заглушка для обработки поиска
  const handleSearch = (e) => {
    setSearchQuery(e.target.value);
    console.log("Поиск:", e.target.value); // Заглушка
  };

  // Заглушка для открытия фильтров
  const handleFilterClick = () => {
    setIsFilterOpen(true);
    console.log("Открыть фильтры"); // Заглушка
  };

  return (
    <div className="quiz-search">
      <div className="quiz-search__container">
        <div className="quiz-search__wrapper">
          <button
            className="quiz-search__filter-btn"
            onClick={handleFilterClick}
            aria-label="Открыть фильтры"
          >
            <SlidersHorizontal className="quiz-search__filter-icon" />
          </button>

          <div className="quiz-search__input-wrapper">
            <Search className="quiz-search__search-icon" />
            <input
              type="text"
              className="quiz-search__input"
              placeholder="Поиск квизов..."
              value={searchQuery}
              onChange={handleSearch}
            />
          </div>
        </div>
      </div>
    </div>
  );
};
