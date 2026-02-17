import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

export function Navbar ({ token, isAdmin, onLogout }) {
    const [isOpen, setIsOpen] = useState(false);
    const navigate = useNavigate();

    const handleLogout = () => {
        onLogout();
        navigate('/login');
    };

    return (
        <nav className="bg-blue-600 text-white shadow-lg">
            <div className="max-w-6xl mx-auto px-4">
                <div className="flex justify-between items-center h-16">
                    <Link to="/" className="font-bold text-xl cursor-pointer">MedPredict</Link>

                    <div className="hidden md:flex items-center space-x-4">
                        {token && (<><Link to="/predict" className="hover:text-blue-200 px-3 py-2">Predict</Link>
                            <Link to="/review" className="hover:text-blue-200 px-3 py-2">Review</Link></>)
                        }

                        {token && isAdmin && (
                            <>
                                <Link to="/invites" className="hover:text-blue-200 px-3 py-2">Invites</Link>
                            </>
                        )}

                        {token ? (
                            <button onClick={handleLogout} className="bg-red-500 hover:bg-red-600 px-4 py-2 rounded transition ml-4">
                                Logout
                            </button>
                        ) : (
                            <Link to="/login" className="bg-green-500 hover:bg-green-600 px-4 py-2 rounded transition">
                                Login
                            </Link>
                        )}
                    </div>

                </div>
            </div>
        </nav>
    );
};