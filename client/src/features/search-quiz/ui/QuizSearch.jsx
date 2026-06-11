import { SearchBar } from '@shared'

export function QuizSearch({ query, onQueryChange }) {
  return (
    <SearchBar
      value={query}
      onChange={onQueryChange}
      placeholder="Поиск по названию или автору..."
    />
  )
}
