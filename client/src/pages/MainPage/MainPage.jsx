import React from "react";
import { Header } from "./../../widgets/Header/Header";
import { UserAction } from "./../../widgets/UserAction/UserAction";
import { QuizeBoard } from "./../../widgets/QuizeBoard/QuizeBoard";
import { Footer } from "./../../widgets/Footer/Footer";
import { QuizSearch } from "../../widgets/QuizSearch/QuizSearch";
export function MainPage() {
  return (
    <>
      {/* <UserAction></UserAction> */}
      <QuizSearch></QuizSearch>
      <QuizeBoard></QuizeBoard>
    </>
  );
}
