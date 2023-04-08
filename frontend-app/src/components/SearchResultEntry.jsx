import React, { useState } from 'react';
import { IoMdArrowDropdown, IoMdArrowDropleft } from 'react-icons/io';

export default function SearchResultEntry({ title, body, answer }) {
    const [opened, setOpen] = useState(false);

    return (
        <div className='entry'
            onClick={() => setOpen(!opened)}
        >
            <div>
                <span>
                    {title}
                </span>
                <button
                    className='entry-toggle'
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
                    <>
                        <p>{body}</p>
                        <p>{answer}</p>
                    </>
                )
            }
        </div>
    )
}