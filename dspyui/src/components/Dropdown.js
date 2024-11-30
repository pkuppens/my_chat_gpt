import React from 'react';

/**
 * Dropdown component to list class names.
 * @param {Object} props - The component props.
 * @param {Array<string>} props.options - The list of class names to display in the dropdown.
 * @param {function} props.onChange - The function to call when the selected class changes.
 * @returns {JSX.Element} The rendered component.
 */
const Dropdown = ({ options, onChange }) => {
  /**
   * Handles the change of the selected class.
   * @param {Object} event - The change event.
   */
  const handleChange = (event) => {
    onChange(event.target.value);
  };

  return (
    <select onChange={handleChange}>
      <option value="">Select a class</option>
      {options.map((option) => (
        <option key={option} value={option}>
          {option}
        </option>
      ))}
    </select>
  );
};

export default Dropdown;
