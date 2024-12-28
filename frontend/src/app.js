import React, { useState } from 'react';
import UploadForm from './components/UploadForm';
import QueryForm from './components/QueryForm';

function App() {
  return (
    <div>
      <h1>Document Management System</h1>
      <UploadForm />
      <QueryForm />
    </div>
  );
}

export default App;
