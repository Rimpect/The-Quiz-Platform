import './App.scss'
import { RouterProvider } from 'react-router-dom'

import { routes } from './app/routes/routes.jsx'
import { Toaster } from 'sonner'

function App() {
  return (
    <>
      <RouterProvider router={routes} />
      <Toaster position="top-right" richColors closeButton duration={3000} />
    </>
  )
}

export default App
