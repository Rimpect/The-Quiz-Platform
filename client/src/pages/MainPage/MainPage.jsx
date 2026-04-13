import React from "react";
import { UserAction } from "./../../widgets/UserAction/UserAction";
import { QuizeBoard } from "./../../widgets/QuizeBoard/QuizeBoard";
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
