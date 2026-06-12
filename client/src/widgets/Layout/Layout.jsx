import { useEffect } from 'react'

import { Outlet, useLocation } from 'react-router-dom'

import { Footer } from '../Footer/Footer'
import { Header } from '../Header'

export function Layout() {
  const { pathname } = useLocation()

  // Скролл наверх при переходе на новую страницу
  useEffect(() => {
    window.scrollTo(0, 0)
  }, [pathname])

  return (
    <>
      <Header></Header>

      <main>
        <Outlet />
      </main>

      <Footer></Footer>
    </>
  )
}
