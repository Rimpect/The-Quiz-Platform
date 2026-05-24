import './App.scss'
import { RouterProvider } from 'react-router-dom'
import { Toaster } from 'sonner'

import { routes } from './routes/routes.jsx'

function App() {
  return (
    <>
      <RouterProvider router={routes} />
      <Toaster position="top-right" richColors closeButton duration={3000} />
    </>
  )
}

export default App
