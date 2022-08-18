import "./App.css";
import React from 'react';
// importing components from react-router-dom package
import {

  Routes,
  Route,
  Navigate,

} from "react-router-dom";
  
// import ImportPage component
import ImportPage from "./components/ImportPage";
// import GraphView
import GraphView from "./components/GraphView";

  
function App() {
  return (
    <>
      {/* This is the alias of BrowserRouter i.e. Router */}
   
        <Routes>
 
          <Route path="/" element={<ImportPage/>} exact/>
            
          {/* This route is for about component 
          with exact path "/about", in component 
          props we passes the imported component*/}
          <Route path="/graph-view" element={<GraphView/>} />
       
            
          {/* If any route mismatches the upper 
          route endpoints then, redirect triggers 
          and redirects app to home component with to="/" */}
        
        </Routes>

    </>
  );
}
  
export default App;