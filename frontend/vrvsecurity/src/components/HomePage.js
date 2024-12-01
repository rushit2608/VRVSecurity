import React from 'react';
import { useNavigate } from "react-router-dom";

function HomePage() {
  const navigate = useNavigate();

  const isAuthenticated = () => {
    return localStorage.getItem('token') !== null; 
  }

  const handleRoleButtonClick = (role) => {
    if (!isAuthenticated()) {
      navigate('/login');
    } else {
      navigate(`/${role.toLowerCase()}-dashboard`); 
    }
  }

  return (
    <div>
      <h1>HomePage</h1>
      <ul>
        <li>
          <button onClick={() => handleRoleButtonClick('Admin')}>Admin</button>
        </li>
        <li>
          <button onClick={() => handleRoleButtonClick('Moderator')}>Moderator</button>
        </li>
        <li>
          <button onClick={() => handleRoleButtonClick('User')}>User</button>
        </li>
      </ul>
    </div>
  );
}

export default HomePage;
