import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Select from 'react-select';

// Set the base URL for axios requests using an environment variable
axios.defaults.baseURL = process.env.REACT_APP_BASE_URL; // Use the baseURL from .env

const ReleaseNotesGenerator = () => {
    // State to store all available sprints fetched from the backend
    const [sprints, setSprints] = useState([]);

    // State to store the sprints that the user selects
    const [selectedSprints, setSelectedSprints] = useState([]);

    // State to manage the loading status (indicates whether the release notes are being generated)
    const [loading, setLoading] = useState(false);

    // State to store the URL of the generated Word document (if successful)
    const [docUrl, setDocUrl] = useState(null);

    // State to manage the notification message and visibility
    const [notification, setNotification] = useState({ message: '', type: '', visible: false });

    // Timeout duration for notifications, fetched from .env or defaulted to 3000ms
    const notificationTimeout = process.env.REACT_APP_NOTIFICATION_TIMEOUT || 3000; // Default to 3000ms if not set

    // Effect hook to fetch the list of sprints when the component mounts
    useEffect(() => {
        const fetchSprints = async () => {
            try {
                // Fetch sprints from the backend API
                const response = await axios.get('/sprints/');
                setSprints(response.data); // Store the fetched sprints in state
            } catch (error) {
                console.error('Error fetching sprints:', error); // Handle error if the request fails
            }
        };

        fetchSprints(); // Call the function to fetch sprints
    }, []); // Empty dependency array ensures the effect runs only once when the component mounts

    // Handler for when the user selects or deselects sprints from the dropdown
    const handleSprintChange = (selectedOptions) => {
        setSelectedSprints(selectedOptions || []); // Update the selected sprints in the state
    };

    // Handler for generating release notes when the "Generate" button is clicked
    const handleGenerate = async () => {
        if (selectedSprints.length === 0) {
            alert('Please select at least one sprint.'); // Alert the user if no sprints are selected
            return;
        }

        setLoading(true); // Set loading to true when the generation starts

        try {
            // Send a POST request to the backend to generate release notes
            const response = await axios.post('/generate/', {
                sprints: selectedSprints.map(option => option.value), // Pass selected sprint names in the request
            }, {
                headers: { 'Content-Type': 'application/json' }, // Set content type as JSON
                responseType: 'blob', // Expect a blob (Word document) as the response
            });

            // Create a URL object from the received blob data (Word document)
            const url = window.URL.createObjectURL(new Blob([response.data], {
                type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', // Word document MIME type
            }));
            setDocUrl(url); // Store the generated document URL in state

            // Set the success notification message and display it
            setNotification({
                message: `Success! HTTP Code: ${response.status}`,
                type: 'success',
                visible: true,
            });

            // Hide the notification after the specified timeout
            setTimeout(() => setNotification({ ...notification, visible: false }), notificationTimeout);

        } catch (error) {
            console.error('Error generating release notes:', error); // Handle any errors during the generation process

            const statusCode = error.response ? error.response.status : 'Unknown'; // Get the HTTP status code from the error response
            setNotification({
                message: `Failure! HTTP Code: ${statusCode}`, // Set failure notification message
                type: 'failure',
                visible: true,
            });

            // Hide the failure notification after the specified timeout
            setTimeout(() => setNotification({ ...notification, visible: false }), notificationTimeout);
        } finally {
            setLoading(false); // Set loading to false when the process is complete (success or failure)
        }
    };

    // Map the list of sprints to the format needed by the react-select component
    const sprintOptions = sprints.map(sprint => ({
        value: sprint.name, // The value is the sprint's name
        label: sprint.name, // The label is displayed to the user
    }));

    return (
        <div className="container">
            <h1>Release Notes Generator</h1>

            {/* Section for selecting sprints */}
            <div>
                <h3>Select Sprints</h3>
                {sprints.length > 0 ? (
                    // React-Select component for multi-select dropdown
                    <Select
                        isMulti
                        options={sprintOptions} // Pass the options for the dropdown
                        value={selectedSprints} // Set the selected values
                        onChange={handleSprintChange} // Handle changes to selection
                        getOptionLabel={(e) => <strong>{e.label}</strong>} // Display the sprint name in bold
                        placeholder="Select sprints..."
                    />
                ) : (
                    <p>Loading sprints...</p> // Show loading text while sprints are being fetched
                )}
            </div>

            {/* Button to trigger release note generation */}
            <div>
                <button onClick={handleGenerate} disabled={loading}>
                    {loading ? (
                        <>
                            Generating... <span className="spinner"></span> {/* Show loading spinner while generating */}
                        </>
                    ) : (
                        'Generate' // Button text when not loading
                    )}
                </button>
            </div>

            {/* Display spinner if loading */}
            {loading && <div className="spinner"></div>}

            {/* Display download link if the document is successfully generated */}
            {docUrl && (
                <div className="document-link">
                    <h3>Release Notes Generated</h3>
                    <a href={docUrl} download="release_notes.docx">
                        Download Word Document
                    </a>
                </div>
            )}

            {/* Notification message */}
            {notification.visible && (
                <div className={`notification ${notification.type}`}>
                    {notification.message} {/* Display success or failure message */}
                </div>
            )}
        </div>
    );
};

export default ReleaseNotesGenerator;
