import React, { useState } from 'react';
import { IoMdArrowDropdown, IoMdArrowDropleft } from 'react-icons/io';

export default function SearchResultEntry({ title, body, answer_body, id }) {
    const [opened, setOpen] = useState(false);
    let link = 'https://english.stackexchange.com/questions/' + id.toString()  ;
    console.log(link);
    answer_body = answer_body == null ? 
                    "There isn't an acceptable answer for this question, try clicking on the link to see the actual question"  
                    : answer_body  
    return (
        <div className='bg-white border-2 border-solid text-left p-2'>
                
                <div className='flex xxs:flex-col xs:flex-row '>
                    <a href={link} target="_blank" className=''>
                    <div className='text-[#ae3737] mr-[1em] hover:text-indigo-500  transition ease-in-out delay-50 hover:-translate-y-1  duration-300 '>
                            {title}
                        </div>
                    </a>
                    <button
                        className='transition bg-[#ae3737] text-white text-[0.8em] hover:bg-indigo-500  delay-50 hover:-translate-y-1  duration-300 '
                        onClick={() => setOpen(!opened)}
                    >
                        {opened ? (
                            "Hide Answer"
                        ) : (
                            "Show Answer"
                        )}
                    </button>
                </div>
                {
                    opened && (
                        <div>
                            {/* <p>{body}</p> */}
                            <p>{answer_body}</p>
                        </div>
                    )
                }
        </div>
    )
}