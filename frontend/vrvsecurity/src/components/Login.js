import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const Login = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        setError("");
        try {

            const config = {
                headers :{
                    "Content-Type" : "application/json",
                },
            };

            const response = await axios.post("http://localhost:8000/api/login/", {
                email,
                password,
            },config);

            console.log(response.data)
            localStorage.setItem("access", response.data.access);
            localStorage.setItem("refresh", response.data.refresh);
            localStorage.setItem("role", response.data.role);
            localStorage.setItem("name", response.data.name);

            const role = response.data.role;
            if (role === "Admin") {
                navigate("/admin_dashboard");
            } else if (role === "Moderator") {
                navigate("/moderator_dashboard");
            } else {
                navigate("/user_dashboard");
            }

        } catch (err) {
            console.log(err)
            setError("Invalid username or password.");
        }
    };

    return (
        <div>
            <h2>Login</h2>
            {error && <p style={{ color: "red" }}>{error}</p>}
            <form onSubmit={handleLogin}>
                <input
                    type="text"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
                <button type="submit">Login</button>
            </form>
        </div>
    );
};

export default Login;
