import { useState } from 'react';
import useApiRequest from './useApiRequest';

export default function useAskQuestion() {

  const { apiRequest, isLoading, error, data } = useApiRequest({
    url: 'http://localhost:5000/ask',
    method: 'POST',
  })
  //   fetch('http://localhost:4389/ask', {
  //   method: 'POST',
  //   headers: {
  //     'Content-Type': 'application/json'
  //   },
  //   body: JSON.stringify({ question: 'What is 3+3?' })
  // })
  const askQuestion = ({ title, body }) => {
    apiRequest({
      body:
        JSON.stringify({ title, body })
    })
  }
  return { askQuestion, isLoading, data };
}
