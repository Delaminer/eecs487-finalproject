import { useState } from 'react';

export default function useApiRequest({url, method = 'POST'}) {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [data, setData] = useState(null);

  async function apiRequest({ body }) {
    setIsLoading(true);
    setError(null);
    setData(null);

    try {
      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
      });
      
      const responseData = await response.json();
      
      setIsLoading(false);
      setData(responseData);
    } catch (error) {
      setIsLoading(false);
      setError(error);
    }
  }

  return {apiRequest, isLoading, error, data};
}
