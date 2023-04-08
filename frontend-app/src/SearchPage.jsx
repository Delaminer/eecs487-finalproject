import React from 'react';
import SearchBar from './components/SearchBar';
import SearchResults from './components/SearchResults';
import QuestionPrompt from './components/QuestionPrompt';
import useAskQuestion from './hooks/useAskQuestion';

export default function SearchPage() {

  const { askQuestion, isLoading, data } = useAskQuestion();

  // const data = [
  //   {
  //     question: "What is 3+3?",
  //     answer: "Because of the properties of mathematics, it is six."
  //   }
  // ]
  return (
    <div className='searchpage'>
      <h1>Ask a Question</h1>
      {/* <SearchBar
        onSearch={(searchTerm) => {
          // use the search term to make a search
          
          // Send API request, and wait to hear back for duplicate questions.
        }}
      /> */}
      <QuestionPrompt
        onAskQuestion={({
          title,
          body,
        }) => {
          console.log("Asking question", title)
          askQuestion({ title, body });
        }

        }
      />
      {
        data && (
          isLoading ? (
            "Loading, please wait"
          ) : (
            <SearchResults data={data.results} />
          )
        )

      }

    </div>
  )
}