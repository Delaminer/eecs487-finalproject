import React, { useState } from 'react';

function SearchBar({ onSearch }) {
  const [query, setQuery] = useState('');

  function handleInputChange(event) {
    setQuery(event.target.value);
  }

  function handleSubmit(event) {
    event.preventDefault();
    onSearch(query);
  }

  return (
    
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Search..."
        value={query}
        onChange={handleInputChange}
        className='searchbar'
      />
      <button type="submit"className='searchbar-button' >
        <img src='search-icon.png' className='searchbar-button-icon'
        onClick={handleSubmit}
        />
      </button>
    </form>
  );
}

export default SearchBar;
