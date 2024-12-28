import React, { useState } from 'react';
import Login from './components/Login';
import Upload from './components/Upload';
import Query from './components/Query';

const App = () => {
  const [token, setToken] = useState(null);

  if (!token) {
    return <Login setToken={setToken} />;
  }

  return (
    <div>
      <h1>Document Management System</h1>
      <Upload token={token} />
      <Query token={token} />
    </div>
  );
};

export default App;
