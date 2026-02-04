import React from "react";
import { Header } from "./../../widgets/Header/Header";
import { UserAction } from "./../../widgets/UserAction/UserAction";
import { QuizeBoard } from "./../../widgets/QuizeBoard/QuizeBoard";
import { Footer } from "./../../widgets/Footer/Footer";
export function MainPage() {
  return (
    <>
      {/* <UserAction></UserAction> */}
      <QuizeBoard></QuizeBoard>
    </>
  );
}
