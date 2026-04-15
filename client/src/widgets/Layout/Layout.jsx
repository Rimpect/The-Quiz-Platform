import { Outlet } from 'react-router-dom'

import { Footer } from '../Footer/Footer'
import { Header } from '../Header/Header'

export function Layout() {
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
