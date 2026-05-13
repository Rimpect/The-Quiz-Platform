import './App.scss'
import { RouterProvider } from 'react-router-dom'

import { routes } from './app/routes/routes.jsx'
import { Layout } from './widgets/Layout/Layout.jsx'

function App() {
  return <RouterProvider router={routes} />
}
export default App
