import React from 'react';

/**
 * Dropdown component to list specifications.
 * @param {Object} props - The component props.
 * @param {Array<string>} props.options - The list of specifications to display in the dropdown.
 * @param {function} props.onChange - The function to call when the selected specification changes.
 * @returns {JSX.Element} The rendered component.
 */
const Dropdown = ({ options, onChange }) => {
  /**
   * Handles the change of the selected specification.
   * @param {Object} event - The change event.
   */
  const handleChange = (event) => {
    onChange(event.target.value);
  };

  return (
    <select onChange={handleChange}>
      <option value="">Select a specification</option>
      {options.map((option) => (
        <option key={option} value={option}>
          {option}
        </option>
      ))}
    </select>
  );
};

export default Dropdown;
