import React from "react";
import "./QuizButton.css";
export function QuizButton({ children, ...attributes }) {
  return (
    <button type="button" className="CustomQuizButton" {...attributes}>
      {children}
    </button>
  );
}
