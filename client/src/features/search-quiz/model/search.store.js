import { create } from 'zustand'

const createInitialFilters = () => ({
  categories: [],
  difficulty: null,
  typeQuestions: [],
  mediaType: [],
  numberOfQuestionsFrom: 1,
  numberOfQuestionsTo: 100,
  durationFrom: 5,
  durationTo: 180,
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
