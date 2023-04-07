import React from 'react';
// import { makeStyles } from '@material-ui/core/styles';
// import AppBar from '@mui/material/AppBar';
// import ToolBar from '@mui/material/ToolBar';
// import Typography from '@mui/material/Typography';
// import TextField from '@mui/material/TextField';
// import TextField from '@mui/material/IconButton';
import { AppBar, Toolbar, Typography, TextField, IconButton, List, ListItem, ListItemText } from '@mui/material';
// import { Search as SearchIcon } from '@material-ui/icons';
import SearchIcon from '@mui/icons-material/Search';

export default function SearchEngine() {
    // const classes = useStyles();
    const [searchText, setSearchText] = React.useState('');
    const [results, setResults] = React.useState([]);
  
    const handleSearch = async (e) => {
      e.preventDefault();
      // call your search function here and update results state
    };
  
    return (
      <div>
        <AppBar position="static">
          <Toolbar>
            <Typography variant="h6">
              My Search Engine
            </Typography>
            <form onSubmit={handleSearch}>
              <div>
                <div>
                  <SearchIcon />
                </div>
                <TextField
                  placeholder="Search…"
                  value={searchText}
                  onChange={e => setSearchText(e.target.value)}
                  inputProps={{ 'aria-label': 'search' }}
                />
              </div>
            </form>
          </Toolbar>
        </AppBar>
        <List>
          {results.map((result, index) => (
            <ListItem key={index}>
              <ListItemText primary={result.title} secondary={result.description} />
            </ListItem>
          ))}
        </List>
      </div>
    );
  }
  