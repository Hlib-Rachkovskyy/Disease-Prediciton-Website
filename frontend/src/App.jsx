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
            {/* Added flex and min-h-screen to push footer down */}
            <div className="flex flex-col min-h-screen bg-gray-50 font-sans text-gray-900">
                <Navbar token={token} isAdmin={isAdmin} onLogout={handleLogout} />

                {/* Main content grows to fill space */}
                <main className="flex-grow container mx-auto px-4 py-8">
                    <Routes>
                        <Route path="/login" element={!token ? <Login setToken={handleLogin} /> : <Navigate to="/predict" />} />
                        <Route path="/register" element={!token ? <Register /> : <Navigate to="/predict" />} />

                        <Route path="/predict" element={token ? <Predict /> : <Navigate to="/login" />} />

                        <Route path="/review" element={token ? <UnapprovedList /> : <Navigate to="/login" />} />
                        <Route path="/invites" element={token && isAdmin ? <AdminInvites /> : <Navigate to="/predict" />} />

                        <Route path="*" element={<Navigate to={token ? "/predict" : "/login"} />} />
                    </Routes>
                </main>

                <footer className="bg-white border-t border-gray-200 py-6 mt-10">
                    <div className="container mx-auto px-4 text-center">
                        <p className="text-gray-600 text-sm mb-2">
                            Made as a <strong>Student Project</strong>
                        </p>
                        <div className="max-w-2xl mx-auto bg-red-50 border border-red-100 p-3 rounded-md">
                            <p className="text-red-700 text-xs leading-relaxed">
                                <strong>Medical Disclaimer:</strong> This application is for educational purposes only.
                                It cannot accurately predict diseases. The results provided are based on a student-level
                                AI model and should not be used for diagnosis.
                                <span className="block mt-1 font-bold italic underline">
                                    Always consult a professional doctor for any health concerns.
                                </span>
                            </p>
                        </div>
                        <p className="text-gray-400 text-[10px] mt-4">
                            &copy; {new Date().getFullYear()} MedPredict Student Project.
                        </p>
                    </div>
                </footer>
            </div>
        </Router>
    );
}

export default App;