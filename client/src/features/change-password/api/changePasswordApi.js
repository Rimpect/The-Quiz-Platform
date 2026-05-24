// export async function changePasswordApi(data) {
//   // позже доделаю до полной версии на axios/fetch
//   return fetch('/api/change-password', {
//     method: 'POST',
//     headers: { 'Content-Type': 'application/json' },
//     body: JSON.stringify(data),
//   })
// }

// Заготовка для бекенда
export async function changePasswordApi(data) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      // имитация успеха
      console.log('MOCK API:', data)

      resolve({
        success: true,
      })

      // или иногда можно имитировать ошибку:
      // reject(new Error('Server error'))
    }, 800)
  })
}
