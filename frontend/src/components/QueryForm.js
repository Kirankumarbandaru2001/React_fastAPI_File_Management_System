import React, { useState } from 'react';
import axios from 'axios';

function QueryForm() {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');

  const handleQueryChange = (e) => {
    setQuery(e.target.value);
  };

  const handleQuerySubmit = async () => {
    const result = await axios.get(`http://localhost:8000/query/ask?query=${query}`);
    setResponse(result.data.response);
  };

  return (
    <div>
      <input type="text" value={query} onChange={handleQueryChange} />
      <button onClick={handleQuerySubmit}>Ask</button>
      <p>{response}</p>
    </div>
  );
}

export default QueryForm;
