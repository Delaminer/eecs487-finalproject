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
      <div className='bar'>
        <input
          type="text"
          placeholder="Search..."
          value={query}
          onChange={handleInputChange}
          className='searchbar'
        />
        <button type="submit"className='searchbar-icon-bubble' >
          <img src='search-icon.png' className='searchbar-icon'
          onClick={handleSubmit}
          ></img>
          </button>
      </div>
    </form>
  );
}

export default SearchBar;
