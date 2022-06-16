import React, { useState } from "react";
import './loginForm.css';
import { Link, Navigate } from "react-router-dom";
import GoogleSSOButton from "../auth/googleSSOButton";
import Student from "../../data/student";

const GoogleSSOLoginForm = () => {
    const [user, _setUser] = useState<Student>(JSON.parse(localStorage.getItem("user") || "null"))

    if (user) {
        return <Navigate to="/application-window"/>
    }

    return (
        <div className="card loginCard">
            <img className="card-img-top" src="../../../nure_se_logo.png" alt="Nure SE logo"></img>
            <div className="card-body d-flex justify-content-center">
                <GoogleSSOButton />
            </div>
            <div className="card-footer text-muted d-flex justify-content-center">
                <Link to="/plain-login" className="text-center">Sign in with email</Link>
            </div>
        </div>
    )
}

export default GoogleSSOLoginForm;