import React, { useState, useEffect } from 'react';
import Dropdown from './components/Dropdown';
import Button from './components/Button';
import { getPrefilledData, getDropdownContent } from './utils/data';

/**
 * Main App component for DSpy Signatures.
 * @returns {JSX.Element} The rendered component.
 */
const App = () => {
  const [selectedSpec, setSelectedSpec] = useState('');
  const [specifications, setSpecifications] = useState([]);
  const [data, setData] = useState({ input: {}, output: {} });

  useEffect(() => {
    const fetchData = async () => {
      const dropdownContent = await getDropdownContent();
      setSpecifications(dropdownContent);
    };
    fetchData();
  }, []);

  /**
   * Parses the specification string into input and output keys.
   * @param {string} specString - The specification string.
   * @returns {Object} The parsed input and output keys.
   */
  const parseSpecification = (specString) => {
    const [input, output] = specString.split('->').map((s) => s.trim());
    const inputKeys = input.split(',').map((s) => s.trim());
    const outputKey = output;
    return { inputKeys, outputKey };
  };

  /**
   * Handles the change of the selected specification.
   * @param {string} specName - The name of the selected specification.
   */
  const handleSpecChange = (specName) => {
    setSelectedSpec(specName);
    const spec = specifications.find((s) => s.name === specName);
    const parsedSpec = parseSpecification(spec.value);
    const prefilledData = getPrefilledData(specName);
    setData({
      input: parsedSpec.inputKeys.reduce((acc, key) => {
        acc[key] = prefilledData[key] || '';
        return acc;
      }, {}),
      output: { [parsedSpec.outputKey]: prefilledData[parsedSpec.outputKey] || '' },
    });
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
      <Dropdown options={specifications.map((spec) => spec.name)} onChange={handleSpecChange} />
      {selectedSpec && (
        <div>
          <div>
            <h2>Input</h2>
            {Object.keys(data.input).map((key) => (
              <div key={key}>
                <label>{key}</label>
                <input type="text" value={data.input[key]} readOnly />
              </div>
            ))}
          </div>
          <Button onClick={handleProcess}>Process</Button>
          <div>
            <h2>Output</h2>
            {Object.keys(data.output).map((key) => (
              <div key={key}>
                <label>{key}</label>
                <input type="text" value={data.output[key]} readOnly />
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default App;
