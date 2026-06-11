import Fuse from 'fuse.js'

const fuseOptions = {
  keys: ['title', 'author'],
  threshold: 0.4, // для админки можно stricter (0.3-0.4)
}

export function useAdminSearch(quizzes, searchQuery) {
  if (!searchQuery.trim()) {
    return quizzes
  }

  const fuse = new Fuse(quizzes, fuseOptions)
  return fuse.search(searchQuery).map((result) => result.item)
}
