import React, { useState, useRef } from 'react';

const FaceRecognition = () => {
    const [file, setFile] = useState(null);
    const [preview, setPreview] = useState('');
    const [results, setResults] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const fileInputRef = useRef(null);

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        if (!file) return;
        
        setFile(file);
        setPreview(URL.createObjectURL(file));
        setResults(null);
        setError('');
    };

    const triggerFileInput = () => {
        fileInputRef.current.click();
    };

    const analyzeFace = async () => {
        if (!file) {
            setError('Please select an image first');
            return;
        }

        setLoading(true);
        const formData = new FormData();
        formData.append('file', file);

        try {
            // Replace with your Render backend URL
            const response = await fetch('https://your-backend.onrender.com/analyze', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Analysis failed');
            }
            
            const data = await response.json();
            setResults(data);
            setError('');
        } catch (err) {
            setError(err.message || 'Error processing image');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container">
            <h1>Moody Mirror 🔥</h1>
            <p>Upload your face and prepare to be roasted!</p>
            
            <div className="upload-section">
                <input 
                    type="file" 
                    accept="image/*" 
                    onChange={handleFileChange}
                    ref={fileInputRef}
                    style={{ display: 'none' }}
                    disabled={loading}
                />
                <button onClick={triggerFileInput} disabled={loading}>
                    Select Image
                </button>
                <button onClick={analyzeFace} disabled={loading || !file}>
                    {loading ? 'Roasting...' : 'Roast My Face!'}
                </button>
            </div>

            {error && <div className="error">{error}</div>}

            <div className="results-container">
                {preview && (
                    <div className="image-preview">
                        <img src={preview} alt="Preview" />
                    </div>
                )}

                {results && (
                    <div className="roast-results">
                        <div className="analysis-results">
                            <p><strong>Age:</strong> {results.age}</p>
                            <p><strong>Mood:</strong> {results.emotion}</p>
                            <p><strong>Gender:</strong> {results.gender}</p>
                            <p><strong>Race:</strong> {results.race}</p>
                        </div>
                        
                        <div className="roast-box">
                            <h3>🔥 Roast of the Day 🔥</h3>
                            <p>{results.roast}</p>
                        </div>
                        
                        <button 
                            className="try-again"
                            onClick={() => {
                                setFile(null);
                                setPreview('');
                                setResults(null);
                                setError('');
                            }}
                        >
                            Try Another Face
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
};

export default FaceRecognition;