import { Outlet } from "react-router-dom";
import { Header } from "../Header/Header";
import { Footer } from "../Footer/Footer";
export function Layout() {
  return (
    <>
      <Header></Header>

      <main>
        <Outlet />
      </main>

      <Footer></Footer>
    </>
  );
}
