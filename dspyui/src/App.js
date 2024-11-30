import React, { useState, useEffect } from 'react';
import Dropdown from './components/Dropdown';
import Button from './components/Button';
import { getPrefilledData, getDropdownContent } from './utils/data';

/**
 * Main App component for DSpy Signatures.
 * @returns {JSX.Element} The rendered component.
 */
const App = () => {
  const [selectedClass, setSelectedClass] = useState('');
  const [fields, setFields] = useState([]);
  const [data, setData] = useState({});

  useEffect(() => {
    const fetchData = async () => {
      const dropdownContent = await getDropdownContent();
      setFields(dropdownContent);
    };
    fetchData();
  }, []);

  /**
   * Handles the change of the selected class.
   * @param {string} className - The name of the selected class.
   */
  const handleClassChange = (className) => {
    setSelectedClass(className);
    const prefilledData = getPrefilledData(className);
    setData(prefilledData);
  };

  /**
   * Handles the processing of the data.
   */
  const handleProcess = () => {
    // Placeholder for processing logic
    console.log('Processing data:', data);
  };

  return (
    <div>
      <h1>DSpy Signatures</h1>
      <Dropdown options={fields} onChange={handleClassChange} />
      {selectedClass && (
        <div>
          {Object.keys(data).map((key) => (
            <div key={key}>
              <label>{key}</label>
              <input type="text" value={data[key]} readOnly />
            </div>
          ))}
        </div>
      )}
      <Button onClick={handleProcess}>Process</Button>
    </div>
  );
};

export default App;
