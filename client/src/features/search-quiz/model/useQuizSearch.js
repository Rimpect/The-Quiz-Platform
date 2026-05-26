import Fuse from 'fuse.js'

import { fuseOptions } from './fuse.config'

export function useQuizSearch(quizzes, query) {
  if (!query.trim()) {
    return quizzes
  }

  const fuse = new Fuse(quizzes, fuseOptions)

  return fuse.search(query).map((result) => result.item)
}
