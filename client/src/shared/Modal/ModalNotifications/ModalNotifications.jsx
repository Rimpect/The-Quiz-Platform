import React from "react";
import { createPortal } from "react-dom";
import "./ModalNotifications.css"
export function ModalNotifications({ open, onClose, children }) {

  if (!open) return null;

  return createPortal(
    <div className="backdrop" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        {children}
      </div>
    </div>,
    document.body
  );
}
