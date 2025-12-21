import React from "react";
import "./SmallButton.css";
export function SmallButton({ children, ...attributes }) {
  return (
    <button type="button" className="CustomSmallButton" {...attributes}>
      {children}
    </button>
  );
}
