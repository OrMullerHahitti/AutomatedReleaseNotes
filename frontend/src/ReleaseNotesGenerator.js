import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Select from 'react-select';
import confetti from 'canvas-confetti'; // Import canvas-confetti

// Set the base URL for axios requests using an environment variable
axios.defaults.baseURL = process.env.REACT_APP_BASE_URL;

const ReleaseNotesGenerator = () => {
    const [sprints, setSprints] = useState([]);
    const [selectedSprints, setSelectedSprints] = useState([]);
    const [loading, setLoading] = useState(false);
    const [docUrl, setDocUrl] = useState(null);
    const [notification, setNotification] = useState({ message: '', type: '', visible: false });
    const notificationTimeout = process.env.REACT_APP_NOTIFICATION_TIMEOUT || 3000;

    useEffect(() => {
        const fetchSprints = async () => {
            try {
                const response = await axios.get('/sprints/');
                setSprints(response.data);
            } catch (error) {
                console.error('Error fetching sprints:', error);
            }
        };

        fetchSprints();
    }, []);

    const handleSprintChange = (selectedOptions) => {
        setSelectedSprints(selectedOptions || []);
    };

    const handleGenerate = async () => {
        if (selectedSprints.length === 0) {
            alert('Please select at least one sprint.');
            return;
        }

        setLoading(true);

        try {
            const response = await axios.post('/generate/', {
                sprints: selectedSprints.map(option => option.value),
            }, {
                headers: { 'Content-Type': 'application/json' },
                responseType: 'blob',
            });

            // Trigger the confetti animation
            confetti({
                particleCount: 100,       // Number of confetti particles
                spread: 70,               // Spread of the confetti
                origin: { x: 0.5, y: 0.5 }, // Origin of the confetti (center of the screen)
            });

            // Create a URL for the Word document
            const url = window.URL.createObjectURL(new Blob([response.data], {
                type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            }));
            setDocUrl(url);

            // Set the success notification
            setNotification({
                message: `Success! HTTP Code: ${response.status}`,
                type: 'success',
                visible: true,
            });

            setTimeout(() => setNotification({ ...notification, visible: false }), notificationTimeout);
        } catch (error) {
            console.error('Error generating release notes:', error);

            const statusCode = error.response ? error.response.status : 'Unknown';
            setNotification({
                message: `Failure! HTTP Code: ${statusCode}`,
                type: 'failure',
                visible: true,
            });

            setTimeout(() => setNotification({ ...notification, visible: false }), notificationTimeout);
        } finally {
            setLoading(false);
        }
    };

    const sprintOptions = sprints.map(sprint => ({
        value: sprint.name,
        label: sprint.name,
    }));

    return (
        <div className="container">
            <h1>Release Notes Generator</h1>
            <div>
                <h3>Select Sprints</h3>
                {sprints.length > 0 ? (
                    <Select
                        isMulti
                        options={sprintOptions}
                        value={selectedSprints}
                        onChange={handleSprintChange}
                        getOptionLabel={(e) => <strong>{e.label}</strong>}
                        placeholder="Select sprints..."
                    />
                ) : (
                    <p>Loading sprints...</p>
                )}
            </div>

            <div>
                <button onClick={handleGenerate} disabled={loading}>
                    {loading ? (
                        <>
                            Generating... <span className="spinner"></span>
                        </>
                    ) : (
                        'Generate'
                    )}
                </button>
            </div>

            {loading && <div className="spinner"></div>}

            {docUrl && (
                <div className="document-link">
                    <h3>Release Notes Generated</h3>
                    <a href={docUrl} download="release_notes.docx">
                        Download Word Document
                    </a>
                </div>
            )}

            {notification.visible && (
                <div className={`notification ${notification.type}`}>
                    {notification.message}
                </div>
            )}
        </div>
    );
};

export default ReleaseNotesGenerator;
