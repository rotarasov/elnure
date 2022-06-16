import React from 'react';
import './App.css';
import { Routes, Route, Navigate } from "react-router-dom";
import SemesterForm from './components/forms/semesterForm';
import PlainLoginForm from './components/forms/plainLoginForm';
import GoogleSSOLoginForm from './components/forms/googleSSOLoginForm';
import ApplicationWindowDetail from './components/applicationWindowDetail';

const PrivateRoute = (props: {children: React.ReactElement}) => {
  const authenticatedUser = localStorage.getItem("user")
  if (!authenticatedUser) {
    return <Navigate to="/login" />
  }
  return props.children
}

function App() {
  return (
    <div className="App">
      <div className="container d-flex justify-content-center align-items-center">
        <Routes>
          <Route path="/login" element={<GoogleSSOLoginForm />}/>
          <Route path="/plain-login" element={<PlainLoginForm />}/>
          <Route 
          path="/application-window" 
          element={
            <PrivateRoute>
              <ApplicationWindowDetail/>
            </PrivateRoute>
          }/>
          <Route 
          path="/semester/:semesterId" 
          element={
            <PrivateRoute>
              <SemesterForm/>
            </PrivateRoute>
          }/>
        </Routes>
      </div>
    </div>
  );
}

export default App;
