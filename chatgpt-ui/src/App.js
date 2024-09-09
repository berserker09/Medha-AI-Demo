import React from 'react';
import Chat from './components/Chat';
import UploadForm from './components/UploadForm';
import './App.css';

function App() {
    return (
        <div className="App">
            <header className="App-header">
                <h1>AI for Students</h1>
                <UploadForm />
                <Chat />
            </header>
        </div>
    );
}

export default App;
