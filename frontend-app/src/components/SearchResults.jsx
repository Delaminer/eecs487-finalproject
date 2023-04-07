import React from 'react';
import SearchResultEntry from './SearchResultEntry';

export default function SearchResults ({ data }) {
    if (!data || data.length == 0) {
        return (
            <></>
        );
    }

    return (
        <div>
            {data.map((elt) => (<SearchResultEntry {...elt} />) )}
        </div>
    )
}