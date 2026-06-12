import { client } from '../client'
import { endpoints } from '../endpoints'

export const mediaService = {
  // Простая загрузка: файл -> URL (без привязки к id сущности)
  uploadSimple: (target, file) => {
    const formData = new FormData()
    formData.append('target', target)
    formData.append('file', file)

    return client('/media/upload-simple', {
      method: 'POST',
      body: formData,
    })
  },

  uploadMedia: (entityType, entityId, file) => {
    const formData = new FormData()
    formData.append('file', file)

    return client(endpoints.media.upload(entityType, entityId), {
      method: 'POST',
      body: formData,
      headers: {
        'Content-Type': undefined,
      },
    })
  },

  uploadMultiple: (entityType, entityId, files) => {
    const formData = new FormData()
    files.forEach((file) => {
      formData.append('files', file)
    })

    return client(endpoints.media.uploadMultiple(entityType, entityId), {
      method: 'POST',
      body: formData,
      headers: {
        'Content-Type': undefined,
      },
    })
  },

  getMediaByPath: (filePath) =>
    client(endpoints.media.byPath(filePath), {
      method: 'GET',
    }),

  getMediaByEntity: (entityType, entityId) =>
    client(endpoints.media.entity(entityType, entityId), {
      method: 'GET',
    }),

  updateMedia: (mediaId, data) =>
    client(endpoints.media.update(mediaId), {
      method: 'PUT',
      body: JSON.stringify(data),
    }),

  deleteMedia: (mediaId) =>
    client(endpoints.media.delete(mediaId), {
      method: 'DELETE',
    }),

  deleteMediaByEntity: (entityType, entityId) =>
    client(endpoints.media.deleteEntity(entityType, entityId), {
      method: 'DELETE',
    }),
}
