// src/components/Chat.js
import React, { useState } from 'react';
import api from '../api/api';
import './Chat.css';

function Chat() {
    const [response, setResponse] = useState('');

    const handleChat = async () => {
        try {
            const res = await api.post('/upload', { text: "Example text" });
            setResponse(res.data.summary);
        } catch (error) {
            console.error(error);
            setResponse('Error occurred while summarizing.');
        }
    };

    return (
        <div className="Chat">
            <button onClick={handleChat}>Summarize</button>
            <p>{response}</p>
        </div>
    );
}

export default Chat;
