export const uploadMedia = (entityType, entityId, formData) =>
  request(`/media/upload/${entityType}/${entityId}`, {
    method: 'POST',
    body: formData,
  })

export const uploadMultipleMedia = (entityType, entityId, formData) =>
  request(`/media/upload-multiple/${entityType}/${entityId}`, {
    method: 'POST',
    body: formData,
  })

export const getEntityMedia = (entityType, entityId) =>
  request(`/media/entity/${entityType}/${entityId}`)

export const deleteMedia = (mediaId) =>
  request(`/media/${mediaId}`, {
    method: 'DELETE',
  })
