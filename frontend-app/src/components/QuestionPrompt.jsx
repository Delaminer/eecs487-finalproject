import React, { useState } from 'react';
import { BiBold, BiItalic, BiLink, BiImage, BiListOl, BiAlignJustify } from "react-icons/bi";
import SearchResults from './SearchResults';

export default function QuestionPrompt({ onAskQuestion, data, isLoading }) {
    const [questionTitle, setQuestionTitle] = useState('');
    const [questionBody, setQuestionBody] = useState('');

    function handleSubmit(event) {
        event.preventDefault();
        onAskQuestion({
            title: questionTitle,
            body: questionBody,
        });
    }

    return (

        <div className='flex-col h-full'>
            <div className=' h-full w-full flex flex-col justify-start   p-[1em] rounded-lg  bg-[white] shadow-xl mb-[1em]'>
                
                <div className='text-xl flex flex-col items-start mb-[0.5em] '>

                    <label className='font-bold'>
                        Title
                    </label>
                    <h3 className='text-[0.8em] '>
                    Be specific and imagine you’re asking a question to another person
                    </h3>
                    <textarea
                        type='text'
                        placeholder="What's your English langauge and usage question? Be specific."
                        value={questionTitle}
                        onChange={e => setQuestionTitle(e.target.value)}
                        className='break-words text-[0.8em] p-[0.5em] rounded-lg w-full border-solid border-gray-400 border-2 '
                    />
                </div>
                <div>

                    {
                        data && (
                        isLoading ? (
                            "Loading, please wait"
                        ) : (
                            <SearchResults data={data.results} />
                            // "hello world"
                        )
                        )

                    }
                </div>
                <div className=' text-xl flex flex-col items-start h-full'>

                    <label className='font-bold'>
                        Body
                    </label>
                    <h3 className='text-[0.8em]'>
                    Include all the information someone would need to answer your question
                    </h3>
                    <div className='flex justify-around text-[1.5em] xs:text-[2em]  border-gray-400 border-2 rounded-t-lg w-full h-fit'>
                        <div className='cursor-pointer'>
                            <BiBold/>
                        </div>
                        <div className='cursor-pointer'>
                            <BiItalic/>
                        </div>
                        <div className='cursor-pointer'>
                            <BiLink/>
                        </div>
                        <div className='cursor-pointer'>
                            <BiImage/>
                        </div>
                        <div className='cursor-pointer'>
                            <BiListOl/>
                        </div>
                        <div className='cursor-pointer'>
                            <BiAlignJustify/>
                        </div>
                    </div>
                    <textarea
                        type='text'
                        value={questionBody}
                        onChange={e => setQuestionBody(e.target.value)}
                        className=' p-[0.5em] focus:border-blue-500 text-start align-top  inline-block rounded-b-lg w-full h-[20em] border-solid border-gray-400 border-2'
                    />
                </div>
            </div>
            <div className='justify-start items-start flex p-[0.5em] text-xl'>

                <button onClick={handleSubmit}  type='submit' className=' rounded-sm shadow-xl bg-[#ae3737] text-white' >
                    {/* <img src='search-icon.png' className='prompt-submit-icon'
                        onClick={handleSubmit}
                    /> */}
                    See Similar questions 
                </button>
            </div>
        </div>
    );
}
