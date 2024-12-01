import React from "react";
import { Navigate } from "react-router-dom";
import { jwtDecode } from 'jwt-decode';

const ProtectedRoute = ({ children, allowedRoles }) => {
    const token = localStorage.getItem("access");

    if (!token) {
        return <Navigate to="/login" />;
    }

    const decodedToken = jwtDecode(token);
    const userRole = localStorage.getItem("role")
    console.log("\n")
    console.log(userRole)

    if (!allowedRoles.includes(userRole)) {
        return <Navigate to="/unauthorized" />;
    }

    return children;
};

export default ProtectedRoute;
