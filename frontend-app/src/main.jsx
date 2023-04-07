import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import SearchPage from './SearchPage'
import './index.css'
import { ThemeProvider, createTheme } from '@mui/material'
import createTypography from '@mui/material/styles/createTypography'
import createPalette from '@mui/material/styles/createPalette'

// const theme = (() => {

//   palette = createPalette({
//     primary: {
//       main: '#576CBC',
//     },
//     secondary: {
//       main: '#A5D7E8',
//     },
//   });

//   typography = createTypography(palette, {
//     fontFamily: '"Comic Sans"',
//   });

//   return createTheme({
//     palette,
//     typography,
//   });
// })();
const theme = createTheme({
  // typography: createTypography(createPalette(), {
  //   fontFamily: '"PT Sans"',
  // })
});

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
      <ThemeProvider theme={theme}>
        <SearchPage />
      </ThemeProvider>
  </React.StrictMode>,
)
