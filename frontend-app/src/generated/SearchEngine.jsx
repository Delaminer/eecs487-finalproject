import React, { useState } from 'react';

// import { makeStyles } from '@material-ui/core/styles';
// import AppBar from '@mui/material/AppBar';
// import ToolBar from '@mui/material/ToolBar';
// import Typography from '@mui/material/Typography';
// import TextField from '@mui/material/TextField';
// import TextField from '@mui/material/IconButton';
import { AppBar, Toolbar, Typography, TextField, IconButton, List, ListItem, ListItemText } from '@mui/material';
// import { Search as SearchIcon } from '@material-ui/icons';
import SearchIcon from '@mui/icons-material/Search';
const styles = {
  root: {
    flexGrow: 1,
  },
  logo: {
    marginRight: 16,
  },
  search: {
    position: 'relative',
    borderRadius: 4,
    backgroundColor: 'white',
    '&:hover': {
      backgroundColor: 'white',
    },
    marginRight: 16,
    marginLeft: 0,
    width: '100%',
    '@media (min-width:600px)': {
      marginLeft: 24,
      width: 'auto',
    },
  },
  searchIcon: {
    padding: 10,
    height: '100%',
    position: 'absolute',
    pointerEvents: 'none',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  inputRoot: {
    color: 'inherit',
  },
  inputInput: {
    padding: '10px 10px 10px 0',
    transition: 'width 300ms cubic-bezier(0.4, 0, 0.2, 1) 0ms',
    width: '100%',
    '@media (min-width:600px)': {
      width: 400,
    },
  },
  list: {
    marginTop: 8,
  },
};
export default function SearchEngine() {
  const [searchText, setSearchText] = useState('');
  const [results, setResults] = useState([]);

  const handleSearch = async (e) => {
    e.preventDefault();
    // call your search function here and update results state
  };

  return (
    <div style={styles.root}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" style={styles.logo}>
            My Search Engine
          </Typography>
          <form onSubmit={handleSearch}>
            <div style={styles.search}>
              <div style={styles.searchIcon}>
                <SearchIcon />
              </div>
              <TextField
                placeholder="Search…"
                value={searchText}
                onChange={e => setSearchText(e.target.value)}
                style={styles.inputInput}
                InputProps={{
                  disableUnderline: true,
                  classes: {
                    root: styles.inputRoot,
                    input: styles.inputInput,
                  },
                }}
              />
            </div>
          </form>
        </Toolbar>
      </AppBar>
      <List style={styles.list}>
        {results.map((result, index) => (
          <ListItem key={index}>
            <ListItemText primary={result.title} secondary={result.description} />
          </ListItem>
        ))}
      </List>
    </div>
  );
}
