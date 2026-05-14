import { StrictMode } from 'react'

import { createRoot } from 'react-dom/client'

import App from './App.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />

    {/* Для github pages использую именно этот, что бы работало без ошибок, когда будет сервер свой то переделать на BrowserRouter */}
  </StrictMode>,
)
