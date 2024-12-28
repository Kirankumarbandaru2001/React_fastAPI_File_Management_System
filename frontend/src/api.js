import axios from 'axios';

const API_URL = 'http://localhost:8000';  // Backend URL

export const login = async (username, password) => {
  const response = await axios.post(`${API_URL}/login`, { username, password });
  return response.data.access_token;
};

export const uploadDocument = async (file, token) => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await axios.post(`${API_URL}/upload`, formData, {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });

  return response.data;
};

export const queryDocument = async (query, token) => {
  const response = await axios.post(
    `${API_URL}/query`,
    { query },
    {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    }
  );
  return response.data;
};
