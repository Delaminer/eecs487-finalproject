import React from 'react';
import SearchBar from './components/SearchBar';
import SearchResults from './components/SearchResults';

export default function SearchPage() {
  const data = [
    {
      title: "What is 3+3?"
    }
  ]
  return (
    <div className='searchpage'>
      <h1>SearchEngine</h1>
      <SearchBar
        onSearch={(searchTerm) =>{
          // use the search term to make a search
          
        }}
      />
      <SearchResults data={data}/>
    </div>
  )
}