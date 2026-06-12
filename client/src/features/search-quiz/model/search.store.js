import { create } from 'zustand'

const createInitialFilters = () => ({
  categories: [],
  difficulty: null,
  typeQuestions: [],
  mediaType: [],
  numberOfQuestionsFrom: 0,
  numberOfQuestionsTo: null,
  durationFrom: 0,
  durationTo: null,
  typeQuiz: null,
})

export const useSearchStore = create((set) => ({
  query: '',
  filter: createInitialFilters(),

  setQuery: (value) => set({ query: value }),
  clearQuery: () => set({ query: '' }),

  setFilter: (newFilters) =>
    set((state) => ({
      filter: {
        ...state.filter,
        ...newFilters,
      },
    })),

  resetFilters: () =>
    set(() => ({
      filter: createInitialFilters(),
    })),

  clearSearch: () =>
    set(() => ({
      query: '',
      filter: createInitialFilters(),
    })),
}))
