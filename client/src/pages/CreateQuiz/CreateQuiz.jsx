import React from "react";
import { QuizHistory } from "../../widgets/QuizHistory/QuizHistory";
import { ProfileStats } from "../../widgets/ProfileStats/ProfileStats";
export default function CreateQuiz() {
  return (
    <>
      <ProfileStats></ProfileStats>
      <QuizHistory></QuizHistory>
    </>
  );
}
