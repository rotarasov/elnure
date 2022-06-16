import React, { useState } from "react";
import './loginForm.css';
import { Link, Navigate } from "react-router-dom";
import { ApiError } from "src/api";
import { plainLogin } from "../../api/users";
import TextInput from "../widgets/textInput";
import SubmitButton from "../widgets/submitButton";
import Student from "../../data/student";

const PlainLoginForm = () => {
    const [errors, setErrors] = useState<string[]>([])
    const [user, setUser] = useState<Student>(JSON.parse(localStorage.getItem("user") || "null"))

    const onSubmit = async (e: React.SyntheticEvent<HTMLElement>) => {
        e.preventDefault();
        const form = e.target as typeof e.target & {
            email: {value: string};
            password: {value: string};
        };
        
        try {
            const user = await plainLogin({email: form.email.value, password: form.password.value})
            localStorage.setItem("user", JSON.stringify(user));
            setUser(user);
        } catch(err) {
            // Body here is error with `detail` field
            setErrors([(err as ApiError).body["detail"]])
        }
    }

    if (user) {
        return <Navigate to="/application-window"/>
    }

    return (
        <div className="card loginCard">
            <img className="card-img-top" src="../../../nure_se_logo.png" alt="Nure SE logo"></img>
            <div className="card-body">
                <form onSubmit={onSubmit}>
                    <h5>Sign in with email and password</h5>
                    <TextInput label="Email" type="email" name="email" />
                    <TextInput label="Password" type="password" name="password" />
                    <SubmitButton label="Sign in" className="btn btn-primary" />
                </form>
            </div>
            <div className="card-footer text-muted d-flex justify-content-center">
                <Link to="/login" className="text-center">Back</Link>
            </div>
        </div>
    )
}

export default PlainLoginForm;