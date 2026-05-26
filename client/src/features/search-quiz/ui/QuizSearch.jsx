import { useMemo, useState } from 'react'

import { SearchBar } from '@shared'

import { useDebounce } from '../model/useDebounce'
import { useQuizSearch } from '../model/useQuizSearch'

export function QuizSearch({ quizzes }) {
  const [query, setQuery] = useState('')

  const debouncedQuery = useDebounce(query)

  const filteredQuizzes = useMemo(() => {
    return useQuizSearch(quizzes, debouncedQuery)
  }, [quizzes, debouncedQuery])

  return (
    <div>
      <SearchBar
        value={query}
        onChange={setQuery}
        placeholder="Поиск по названию или автору..."
      />

      <div>
        {filteredQuizzes.length === 0 ? (
          <p>Ничего не найдено</p>
        ) : (
          filteredQuizzes.map((quiz) => (
            <div key={quiz.id}>
              <h3>{quiz.title}</h3>
              <p>{quiz.author}</p>
            </div>
          ))
        )}
      </div>
    </div>
  )
}
