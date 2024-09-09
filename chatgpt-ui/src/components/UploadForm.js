// src/components/UploadForm.js
import React, { useState } from 'react';
import api from '../api/api';
import './UploadForm.css';

function UploadForm() {
    const [file, setFile] = useState(null);
    const [summary, setSummary] = useState('');
    const [error, setError] = useState('');

    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
    };

    const handleUpload = async (event) => {
        event.preventDefault();
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);

        try {
            const res = await api.post('/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            setSummary(res.data.summary);
            setError('');
        } catch (error) {
            console.error(error);
            setSummary('');
            setError('Error occurred while processing the file.');
        }
    };

    return (
        <div className="UploadForm">
            <form onSubmit={handleUpload}>
                <input type="file" onChange={handleFileChange} />
                <button type="submit">Upload</button>
            </form>
            {summary && <p>{summary}</p>}
            {error && <p className="error">{error}</p>}
        </div>
    );
}

export default UploadForm;
