import './App.scss'

import { ErrorBoundary } from '@shared'
import { RouterProvider } from 'react-router-dom'
import { Toaster } from 'sonner'

import { router } from './routes/routes.jsx'

function App() {
  return (
    <ErrorBoundary>
      <RouterProvider router={router} />
      <Toaster position="top-right" richColors closeButton duration={3000} />
    </ErrorBoundary>
  )
}

export default App
