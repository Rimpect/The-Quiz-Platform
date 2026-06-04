import './App.scss'
import { useEffect } from 'react'

import { RouterProvider } from 'react-router-dom'
import { Toaster } from 'sonner'

import useTheme from '../features/theme-toggle/hooks/useTheme'

import { router } from './routes/routes.jsx'

function App() {
  const { isDarkTheme } = useTheme()

  useEffect(() => {
    if (isDarkTheme) {
      document.documentElement.classList.add('dark-theme')
      document.documentElement.classList.remove('light-theme')
    } else {
      document.documentElement.classList.add('light-theme')
      document.documentElement.classList.remove('dark-theme')
    }
  }, [isDarkTheme])

  return (
    <>
      <RouterProvider router={router} />
      <Toaster position="top-right" richColors closeButton duration={3000} />
    </>
  )
}

export default App
