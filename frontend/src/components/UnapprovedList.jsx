import React, { useEffect, useState } from 'react';
import api from '../api';

const UnapprovedList = () => {
    const [diseases, setDiseases] = useState([]);
    const [loading, setLoading] = useState(true);

    const [editingId, setEditingId] = useState(null);
    const [editName, setEditName] = useState("");

    const fetchDiseases = async () => {
        try {
            const response = await api.get('/list');
            if (response.data && response.data['List of diseases']) {
                setDiseases(response.data['List of diseases']);
            }
        } catch (err) {
            console.error("Failed to fetch list");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchDiseases();
    }, []);

    const startEditing = (disease) => {
        setEditingId(disease.Id);
        setEditName(disease.Name);
    };

    const handleApprove = async (id) => {
        if (!editName.trim()) return;

        try {
            await api.post(`/disease/specify/${id}/${editName}`);
            setDiseases(prev => prev.filter(d => d.Id !== id));
            setEditingId(null);
        } catch (err) {
            alert("Error approving disease. You might not have permission.");
        }
    };

    if (loading) return <div>Loading...</div>;

    return (
        <div className="max-w-4xl mx-auto bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-2xl font-bold mb-6 text-gray-800">Unapproved Reports</h2>

            {diseases.length === 0 ? (
                <p className="text-gray-500">No unapproved diseases found.</p>
            ) : (
                <ul className="divide-y divide-gray-200">
                    {diseases.map((disease) => (
                        <li key={disease.Id} className="py-4 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">

                            <div className="flex-1">
                                {editingId === disease.Id ? (
                                    <input
                                        type="text"
                                        value={editName}
                                        onChange={(e) => setEditName(e.target.value)}
                                        className="border-2 border-indigo-500 rounded px-2 py-1 w-full text-lg font-bold outline-none"
                                        autoFocus
                                    />
                                ) : (
                                    <p className="font-bold text-lg">{disease.Name}</p>
                                )}
                                <p className="text-sm text-gray-500">{disease.Description}</p>
                            </div>

                            <div className="flex gap-2">
                                {editingId === disease.Id ? (
                                    <>
                                        <button
                                            onClick={() => handleApprove(disease.Id)}
                                            className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 font-medium"
                                        >
                                            Confirm
                                        </button>
                                        <button
                                            onClick={() => setEditingId(null)}
                                            className="bg-gray-200 text-gray-700 px-4 py-2 rounded hover:bg-gray-300"
                                        >
                                            Cancel
                                        </button>
                                    </>
                                ) : (
                                    <button
                                        onClick={() => startEditing(disease)}
                                        className="bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700 transition-colors"
                                    >
                                        Review
                                    </button>
                                )}
                            </div>

                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default UnapprovedList;