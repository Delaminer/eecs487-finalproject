import React from 'react';
import SearchResultEntry from './SearchResultEntry';

export default function SearchResults ({ data }) {
    // if (!data) return null;
    // data = [data];
    if (!data || data.length == 0) {
        return (
            <></>
        );
    }

    return (
        <div className='xxs:text-[0.8em] border-2 border-gray-400 border-solid mb-[1em] rounded'>
            
            <div className='bg-gray-200 border-[0.05em] border-b-gray-400 rounded-t border-solid'>
                Similar Questions 
            </div>
            <div className='overflow-y-auto h-[10em]'>
                {data.map((elt) => (<SearchResultEntry {...elt} />) )}
            </div>
        </div>
    )
}