import './App.scss'
import { useEffect } from 'react'

import { useAuthStore } from '@entities'
import { ErrorBoundary } from '@shared'
import { RouterProvider } from 'react-router-dom'
import { Toaster, toast } from 'sonner'

import { router } from './routes/routes.jsx'

function App() {
  useEffect(() => {
    const onExpired = () => {
      const { isAuthenticated, token } = useAuthStore.getState()
      if (!isAuthenticated && !token) return
      useAuthStore.setState({
        token: null,
        refreshToken: null,
        user: null,
        isAuthenticated: false,
      })
      toast.info('Сессия истекла, войдите снова')
    }
    window.addEventListener('auth:expired', onExpired)
    return () => window.removeEventListener('auth:expired', onExpired)
  }, [])

  return (
    <ErrorBoundary>
      <RouterProvider router={router} />
      <Toaster position="top-right" richColors closeButton duration={3000} />
    </ErrorBoundary>
  )
}

export default App
