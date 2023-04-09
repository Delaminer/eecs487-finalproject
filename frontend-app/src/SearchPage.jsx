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
    <div className='absolute top-0 left-0 right-0 bottom-0 bg-[#fcfaf3] '> 
      <div className='flex-col mt-[1em]  xs:mx-[4em] mx-[1em] '>
        
        <div className='text-left text-[0.5em] font-bold	'>

          <h1 className='px-[0.5em]'>
            Ask a question
          </h1>
        </div>
        {/* <SearchBar
          onSearch={(searchTerm) => {
            // use the search term to make a search
            
            // Send API request, and wait to hear back for duplicate questions.
          }}
        /> */}
        <div className=' h-fit mt-[1em] mb-[2em]  '>
          {/* Need two more divs below, one for title and one for questions  */}

          <QuestionPrompt
            data={data} isLoading={isLoading} onAskQuestion={({
              title,
              body,
            }) => {
              console.log("Asking question", title)
              askQuestion({ title, body });
            }

            }
          />
          
        </div>
      </div>

    </div>
  )
}