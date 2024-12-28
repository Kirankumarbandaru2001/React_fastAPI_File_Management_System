import React, { useState } from 'react';
import { uploadDocument } from '../api';

const Upload = ({ token }) => {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (file) {
      try {
        const response = await uploadDocument(file, token);
        setMessage(response.message);
      } catch (err) {
        setMessage('Error uploading document');
      }
    } else {
      setMessage('No file selected');
    }
  };

  return (
    <div>
      <h2>Upload Document</h2>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload</button>
      {message && <p>{message}</p>}
    </div>
  );
};

export default Upload;
