import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./components/Login";
import Signup from "./components/SignUp";
import {
  AdminDashboard,
  ModeratorDashboard,
  UserDashboard,
} from "./components/DashboardPages";
import ProtectedRoute from "./components/ProtectedRoute";
import HomePage from "./components/HomePage";


const App = () => {
  return (
    <Router>
      <Routes>
      <Route path="/" element={<HomePage />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/login" element={<Login />} />
        <Route
          path="/admin_dashboard"
          element={
            <ProtectedRoute allowedRoles={["Admin"]}>
              <AdminDashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/moderator_dashboard"
          element={
            <ProtectedRoute allowedRoles={["Moderator"]}>
              <ModeratorDashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/user_dashboard"
          element={
            <ProtectedRoute allowedRoles={["User", "Admin"]}>
              <UserDashboard />
            </ProtectedRoute>
          }
        />
      </Routes>
    </Router>
  );
};

export default App;
