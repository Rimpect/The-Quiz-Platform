
export async function changePasswordApi(data) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      console.log('MOCK API:', data)

      resolve({
        success: true,
      })

      reject(new Error('Server error'))
    }, 800)
  })
}
