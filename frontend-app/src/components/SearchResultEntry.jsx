import React, { useState } from 'react';
import { IoMdArrowDropdown, IoMdArrowDropleft } from 'react-icons/io';

export default function SearchResultEntry({ title, body, answer }) {
    const [opened, setOpen] = useState(false);

    return (
        <div className='bg-white border-2 border-solid text-left p-2'>
                
            <div className='flex xxs:flex-col xs:flex-row'>
                <span className='text-[#ae3737] mr-[1em]'>
                    {title}
                </span>
                <button
                    className='bg-[#ae3737] text-white text-[0.8em] '
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
                    <div className='text-[0.95em]'>
                        <p>{body}</p>
                        <p>{answer}</p>
                    </div>
                )
            }
        </div>
    )
}