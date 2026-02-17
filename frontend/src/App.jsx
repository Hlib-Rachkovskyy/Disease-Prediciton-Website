import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Navbar } from './components/Navbar';
import Login from './components/Login';
import Register from './components/Register';
import Predict from './components/Predict';
import UnapprovedList from './components/UnapprovedList.jsx';
import AdminInvites from './components/AdminInvites';

function App() {
    const [token, setToken] = useState(localStorage.getItem('token'));
    const [isAdmin, setIsAdmin] = useState(localStorage.getItem('username') === 'admin');

    const handleLogout = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('username');
        setToken(null);
        setIsAdmin(false);
    };

    const handleLogin = (newToken, username) => {
        localStorage.setItem('token', newToken);
        localStorage.setItem('username', username);
        setToken(newToken);
        setIsAdmin(username === 'admin');
    };

    return (
        <Router>
            <div className="min-h-screen bg-gray-50 font-sans text-gray-900">
                <Navbar token={token} isAdmin={isAdmin} onLogout={handleLogout} />

                <div className="container mx-auto px-4 py-8">
                    <Routes>
                        <Route path="/login" element={!token ? <Login setToken={handleLogin} /> : <Navigate to="/predict" />} />
                        <Route path="/register" element={!token ? <Register /> : <Navigate to="/predict" />} />

                        <Route path="/predict" element={token ? <Predict /> : <Navigate to="/login" />} />

                        <Route path="/review" element={token ? <UnapprovedList /> : <Navigate to="/login" />} />
                        <Route path="/invites" element={token && isAdmin ? <AdminInvites /> : <Navigate to="/predict" />} />

                        <Route path="*" element={<Navigate to={token ? "/predict" : "/login"} />} />
                    </Routes>
                </div>
            </div>
        </Router>
    );
}

export default App;