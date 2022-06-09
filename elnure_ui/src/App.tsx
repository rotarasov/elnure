import React from 'react';
import { Routes, Route, Link } from "react-router-dom";
import GoogleSSOButton from './components/auth/googleSSOButton';
import DefaultStragetyChoiceForm from './components/forms/defaultStrategyChoiceForm';

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<DefaultStragetyChoiceForm/>}/>
      </Routes>
    </div>
  );
}

export default App;
