import React, { useState } from 'react';
import api from '../api';
import { useNavigate, Link } from 'react-router-dom';

const Login = ({ setToken }) => {
    const [formData, setFormData] = useState({ username: '', password: '' });
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await api.post('/login', formData);

            const token = Object.values(response.data)[0];
            localStorage.setItem('username', response.data.username);
            localStorage.setItem('token', token);

            setToken(token);
            navigate('/predict');
        } catch (err) {
            setError('Invalid username or password');
        }
    };

    return (
        <div className="max-w-md mx-auto bg-white p-8 rounded-xl shadow-md">
            <h2 className="text-2xl font-bold mb-6 text-center">Login</h2>
            {error && <div className="bg-red-100 text-red-700 p-3 rounded mb-4">{error}</div>}

            <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                    <label className="block text-sm font-medium text-gray-700">Username</label>
                    <input
                        type="text"
                        className="mt-1 block w-full p-2 border rounded-md"
                        value={formData.username}
                        onChange={(e) => setFormData({...formData, username: e.target.value})}
                    />
                </div>
                <div>
                    <label className="block text-sm font-medium text-gray-700">Password</label>
                    <input
                        type="password"
                        className="mt-1 block w-full p-2 border rounded-md"
                        value={formData.password}
                        onChange={(e) => setFormData({...formData, password: e.target.value})}
                    />
                </div>
                <button type="submit" className="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700">
                    Sign In
                </button>
            </form>
            <p className="mt-4 text-center text-sm">
                Don't have an account? <Link to="/register" className="text-blue-600">Register</Link>
            </p>
        </div>
    );
};

export default Login;