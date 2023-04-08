import { useState, useEffect } from 'react';

function useCachedApi(apiFunction, cacheTime) {
  const [data, setData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const cachedData = localStorage.getItem('cachedData');
    const cachedTimestamp = localStorage.getItem('cachedTimestamp');

    if (cachedData && cachedTimestamp && Date.now() - cachedTimestamp < cacheTime) {
      setData(JSON.parse(cachedData));
      setIsLoading(false);
    } else {
      apiFunction()
        .then(result => {
          setData(result);
          setIsLoading(false);
          localStorage.setItem('cachedData', JSON.stringify(result));
          localStorage.setItem('cachedTimestamp', Date.now());
        })
        .catch(error => {
          console.error(error);
          setIsLoading(false);
        });
    }
  }, [apiFunction, cacheTime]);

  return { data, isLoading };
}
