import { mediaService } from '@shared'
import { create } from 'zustand'

export const useMediaStore = create((set) => ({
  media: [],
  isLoading: false,
  error: null,

  uploadMedia: async (entityType, entityId, file) => {
    set({ isLoading: true, error: null })
    try {
      const result = await mediaService.uploadMedia(entityType, entityId, file)
      set({ isLoading: false })
      return result
    } catch (err) {
      set({ error: err.message, isLoading: false })
      throw err
    }
  },

  uploadMultiple: async (entityType, entityId, files) => {
    set({ isLoading: true, error: null })
    try {
      const result = await mediaService.uploadMultiple(
        entityType,
        entityId,
        files,
      )
      set({ isLoading: false })
      return result
    } catch (err) {
      set({ error: err.message, isLoading: false })
      throw err
    }
  },

  fetchMediaByEntity: async (entityType, entityId) => {
    set({ isLoading: true, error: null })
    try {
      const media = await mediaService.getMediaByEntity(entityType, entityId)
      set({ media, isLoading: false })
      return media
    } catch (err) {
      set({ error: err.message, isLoading: false })
      throw err
    }
  },

  updateMedia: async (mediaId, data) => {
    set({ isLoading: true, error: null })
    try {
      const result = await mediaService.updateMedia(mediaId, data)
      set({ isLoading: false })
      return result
    } catch (err) {
      set({ error: err.message, isLoading: false })
      throw err
    }
  },

  deleteMedia: async (mediaId) => {
    set({ isLoading: true, error: null })
    try {
      await mediaService.deleteMedia(mediaId)
      set((state) => ({
        media: state.media.filter((m) => m.id !== mediaId),
        isLoading: false,
      }))
    } catch (err) {
      set({ error: err.message, isLoading: false })
      throw err
    }
  },

  deleteMediaByEntity: async (entityType, entityId) => {
    set({ isLoading: true, error: null })
    try {
      await mediaService.deleteMediaByEntity(entityType, entityId)
      set({ media: [], isLoading: false })
    } catch (err) {
      set({ error: err.message, isLoading: false })
      throw err
    }
  },

  clearError: () => set({ error: null }),
}))
