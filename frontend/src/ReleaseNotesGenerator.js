import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Select from 'react-select';
import confetti from 'canvas-confetti';

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

                let errorMessage = 'An error occurred while fetching sprints.';

                if (error.code === 'ECONNABORTED') {
                    errorMessage = 'Request timed out. Please try again later.';
                } else if (!error.response) {
                    errorMessage = 'Unable to reach the backend service. Please try again later.';
                } else if (error.response) {
                    const statusCode = error.response.status;
                    errorMessage = `Failed to load sprints. HTTP Code: ${statusCode}`;
                }

                // Use a functional update to set the notification
                setNotification((prevNotification) => ({
                    ...prevNotification,
                    message: errorMessage,
                    type: 'failure',
                    visible: true,
                }));

                // Clear notification after the specified timeout
                setTimeout(() => setNotification((prevNotification) => ({ ...prevNotification, visible: false })), notificationTimeout);
            }
        };

        fetchSprints();
    }, [notificationTimeout]); // Only include notificationTimeout, no need to include 'notification'

    const handleSprintChange = (selectedOptions) => {
        setSelectedSprints(selectedOptions || []);
    };

    const handleGenerate = async () => {
        if (selectedSprints.length === 0) {
            alert('Please select at least one sprint.');
            return;
        }

        setDocUrl(null);  // Clear any previous docUrl
        setNotification({ message: '', type: '', visible: false });  // Clear previous notification

        setLoading(true);

        try {
            const response = await axios.post('/generate/', {
                sprints: selectedSprints.map(option => option.value),
            }, {
                headers: { 'Content-Type': 'application/json' },
                responseType: 'blob',
            });

            // Trigger confetti animation
            confetti({
                particleCount: process.env.REACT_APP_CONFETTI_PARTICLE_COUNT,
                spread: process.env.REACT_APP_CONFETTI_SPREAD,
                origin: { x: 0.5, y: 0.5 },
            });

            const url = window.URL.createObjectURL(new Blob([response.data], {
                type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            }));
            setDocUrl(url);

            // Use a functional update to set the notification
            setNotification((prevNotification) => ({
                ...prevNotification,
                message: `Success! HTTP Code: ${response.status}`,
                type: 'success',
                visible: true,
            }));

            // Clear notification after the specified timeout
            setTimeout(() => setNotification((prevNotification) => ({ ...prevNotification, visible: false })), notificationTimeout);
        } catch (error) {
            console.error('Error generating release notes:', error);

            let errorMessage = 'An error occurred while generating release notes.';

            if (error.code === 'ECONNABORTED') {
                errorMessage = 'Request timed out. Please try again later.';
            } else if (!error.response) {
                errorMessage = 'Unable to reach the backend service. Please try again later.';
            } else if (error.response) {
                const statusCode = error.response.status;
                errorMessage = `Failure! HTTP Code: ${statusCode}`;
            }

            // Use a functional update to set the notification
            setNotification((prevNotification) => ({
                ...prevNotification,
                message: errorMessage,
                type: 'failure',
                visible: true,
            }));

            // Clear notification after the specified timeout
            setTimeout(() => setNotification((prevNotification) => ({ ...prevNotification, visible: false })), notificationTimeout);
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
                        isDisabled={loading}  // Disable the dropdown while loading
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
