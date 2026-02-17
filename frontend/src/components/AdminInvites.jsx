import React, { useState } from 'react';
import api from '../api';

const AdminInvites = () => {
    const [amount, setAmount] = useState(1);
    const [generatedInvites, setGeneratedInvites] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const handleCreateInvites = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError("");

        try {
            const response = await api.post(`/invites/${amount}`);

            const newInvites = response.data['Invites: '] || response.data['Invites'];
            setGeneratedInvites(newInvites);
        } catch (err) {
            setError(err.response?.data?.['Not enough right\'s']
                ? "Unauthorized: Admin access required."
                : "Failed to generate invites.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-2xl mx-auto bg-white p-6 rounded-lg shadow-md mt-8">
            <h2 className="text-2xl font-bold mb-4">Generate Invites</h2>

            <form onSubmit={handleCreateInvites} className="flex items-end gap-4 mb-6">
                <div className="flex-1">
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                        Number of Invites
                    </label>
                    <input
                        type="number"
                        min="1"
                        max="50"
                        value={amount}
                        onChange={(e) => setAmount(e.target.value)}
                        className="w-full border border-gray-300 rounded px-3 py-2 outline-indigo-500"
                    />
                </div>
                <button
                    type="submit"
                    disabled={loading}
                    className="bg-indigo-600 text-white px-6 py-2 rounded hover:bg-indigo-700 disabled:bg-gray-400 transition-colors"
                >
                    {loading ? "Generating..." : "Generate"}
                </button>
            </form>

            {error && <p className="text-red-500 mb-4 text-sm">{error}</p>}

            {generatedInvites.length > 0 && (
                <div className="bg-gray-50 border border-gray-200 rounded p-4">
                    <h3 className="font-semibold mb-2">Generated Codes:</h3>
                    <div className="grid grid-cols-1 gap-2">
                        {generatedInvites.map((code, index) => (
                            <div key={index} className="bg-white border rounded px-3 py-2 flex justify-between items-center group">
                                <code className="text-indigo-700 font-mono">{code}</code>
                                <button
                                    onClick={() => navigator.clipboard.writeText(code)}
                                    className="text-xs text-gray-400 hover:text-indigo-600 opacity-0 group-hover:opacity-100 transition-opacity"
                                >
                                    Copy
                                </button>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};

export default AdminInvites;