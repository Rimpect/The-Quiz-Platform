export async function deleteAccount() {
  // MOCK API

  return new Promise((resolve, reject) => {
    setTimeout(() => {
      const isSuccess = true

      if (isSuccess) {
        resolve({
          success: true,
          message: 'Аккаунт удален',
        })
      } else {
        reject(new Error('Ошибка удаления аккаунта'))
      }
    }, 1000)
  })
}
