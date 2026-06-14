import { Suspense, useLayoutEffect } from 'react'

import { Outlet, useLocation } from 'react-router-dom'

import { Footer } from '../Footer/Footer'
import { Header } from '../Header'

export function Layout() {
  const { pathname } = useLocation()

  // Скролл наверх при переходе на новую страницу.
  // behavior:'instant' перебивает глобальный scroll-behavior: smooth —
  // иначе на телефоне переход «анимируется» и тупит. useLayoutEffect —
  // чтобы прыжок наверх случился до отрисовки новой страницы.
  useLayoutEffect(() => {
    window.scrollTo({ top: 0, left: 0, behavior: 'instant' })
  }, [pathname])

  return (
    <>
      <Header></Header>

      <main>
        <Suspense
          fallback={
            <div style={{ padding: '2rem', textAlign: 'center' }}>
              Загрузка…
            </div>
          }
        >
          <Outlet />
        </Suspense>
      </main>

      <Footer></Footer>
    </>
  )
}
