import React from 'react';

export default function SearchResultEntry ({ title }) {

    return (
        <div className='entry'>
            <span>
                {title}
            </span>
            <span>
                Learn More
            </span>
        </div>
    )
}