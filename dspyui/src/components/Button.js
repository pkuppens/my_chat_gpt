import React from 'react';

/**
 * Button component to invoke processing.
 * @param {Object} props - The component props.
 * @param {function} props.onClick - The function to call when the button is clicked.
 * @param {React.ReactNode} props.children - The content to display inside the button.
 * @returns {JSX.Element} The rendered component.
 */
const Button = ({ onClick, children }) => {
  return (
    <button onClick={onClick}>
      {children}
    </button>
  );
};

export default Button;
