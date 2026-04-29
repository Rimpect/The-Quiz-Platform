import { StrictMode } from 'react'

import { createRoot } from 'react-dom/client'
import { HashRouter } from 'react-router-dom'

import App from './App.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <HashRouter>
      <App />
    </HashRouter>
    {/* Для github pages использую именно этот, что бы работало без ошибок, когда будет сервер свой то переделать на BrowserRouter */}
  </StrictMode>,
)
