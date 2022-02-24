import React, { useEffect, useState}  from "react";
import Navbar from './Navbar';
import Detection from './Detection';
import Classify from './Classify';
import Dataset from './Dataset';
import Parameter from './Parameter';
import Mainpage from './Mainpage';
import Training from "./training";
import Process from "./process";
//var resumable = require('./resumable.js-master/samples/Node.js/resumable-node.js')
import { BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import {
  Nav,
  NavDropdown,
  Form,
  FormControl,
  Button,
  Table
 } from "react-bootstrap"
import Upload from "./upload";

function App() {
 
  return (
    <Router>
      <div className="App">
        <Navbar />
        <div className="content">
       
          <Routes>
          <Route exact path="/mainpage"  element={<Mainpage />} >
            </Route>
            <Route exact path="/detection" element={<Detection/>} >
            </Route>
            <Route path="/classify" element={ <Classify/>} >
            </Route>
            <Route path="/Dataset" element={<Dataset/>} >
              </Route>
            <Route path="/parameter" element={<Parameter/>} >
            </Route>
            <Route path="/training" element={<Training/>} >
            </Route>
            <Route path="/upload" element={<Upload/>} >
            </Route>
            <Route path="/process" element={<Process/>} >
            </Route>
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
