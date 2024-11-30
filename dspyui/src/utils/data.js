/**
 * Retrieves pre-filled data based on the specification name.
 * @param {string} specName - The name of the specification.
 * @returns {Object} The pre-filled data for the specification.
 */
export const getPrefilledData = (specName) => {
  // Placeholder function to retrieve pre-filled data based on specification name
  const data = {
    // 'SpecA': { query: 'What is AI?', context: 'Artificial Intelligence', answer: 'AI is the simulation of human intelligence in machines.' },
    'SpecB': { query: 'What is ML?', context: 'Machine Learning', answer: 'ML is a subset of AI that involves training algorithms on data.' },
  };
  return data[specName] || {};
};

/**
 * Retrieves the content for the dropdown.
 * @returns {Promise<Array<Object>>} A promise that resolves to an array of specifications.
 */
export const getDropdownContent = async () => {
  // Placeholder function to retrieve dropdown content
  return [
    { name: 'SpecA', value: 'sentence -> sentiment' },
    { name: 'SpecB', value: 'query, context -> answer' },
  ];
};
