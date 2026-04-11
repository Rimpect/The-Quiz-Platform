// AverageButton.jsx
export function AverageButton({ 
  children, 
  onClick, 
  disabled = false, 
  variant = "primary",
  className = "",
  ...props 
}) {
  const baseStyles = {
    padding: "12px 24px",
    border: "none",
    borderRadius: "8px",
    cursor: "pointer",
    fontSize: "16px",
    fontWeight: "500",
    transition: "all 0.3s ease",
    fontFamily: "inherit",
    display: "inline-flex",
    alignItems: "center",
    justifyContent: "center",
    gap: "8px",
    textDecoration: "none",
    minWidth: "140px"
  };

  const variants = {
    primary: {
      background: "linear-gradient(135deg, #3498db, #2980b9)",
      color: "white",
      boxShadow: "0 4px 15px rgba(52, 152, 219, 0.3)"
    },
    secondary: {
      background: "#f8f9fa",
      color: "#333",
      border: "2px solid #dee2e6"
    },
    outline: {
      background: "transparent",
      color: "#3498db",
      border: "2px solid #3498db"
    },
    success: {
      background: "linear-gradient(135deg, #4CAF50, #45a049)",
      color: "white",
      boxShadow: "0 4px 15px rgba(76, 175, 80, 0.3)"
    }
  };

  const disabledStyles = {
    opacity: "0.6",
    cursor: "not-allowed",
    transform: "none !important"
  };

  const buttonStyles = {
    ...baseStyles,
    ...variants[variant],
    ...(disabled ? disabledStyles : {}),
    ...props.style
  };

  return (
    <button
      style={buttonStyles}
      onClick={onClick}
      disabled={disabled}
      className={`average-button ${className}`}
      {...props}
    >
      {children}
    </button>
  );
}