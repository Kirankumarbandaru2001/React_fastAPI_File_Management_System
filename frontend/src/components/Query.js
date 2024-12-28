import React, { useState } from 'react';
import { queryDocument } from '../api';

const Query = ({ token }) => {
  const [query, setQuery] = useState('');
  const [answer, setAnswer] = useState('');

  const handleQuery = async () => {
    try {
      const response = await queryDocument(query, token);
      setAnswer(response.response);
    } catch (err) {
      setAnswer('Error querying document');
    }
  };

  return (
    <div>
      <h2>Query Document</h2>
      <input
        type="text"
        placeholder="Ask a question"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <button onClick={handleQuery}>Ask</button>
      {answer && <p>{answer}</p>}
    </div>
  );
};

export default Query;
