import React, { useState, useEffect } from 'react';
import axios from 'axios';

axios.defaults.baseURL = 'http://127.0.0.1:8000'; // set up the backend URL globally

const ReleaseNotesGenerator = () => {
    const [sprints, setSprints] = useState([]);
    const [selectedSprints, setSelectedSprints] = useState([]);
    const [loading, setLoading] = useState(false);
    const [docUrl, setDocUrl] = useState(null);

    // Fetch sprints from the backend
    useEffect(() => {
        const fetchSprints = async () => {
            try {
                const response = await axios.get('/sprints/');
                setSprints(response.data); // assuming response.data is the list of sprints
            } catch (error) {
                console.error('Error fetching sprints:', error);
            }
        };

        fetchSprints();
    }, []);

    // Handle sprint selection change
    const handleSprintChange = (event) => {
        const value = event.target.value;
        setSelectedSprints((prevSelectedSprints) =>
            prevSelectedSprints.includes(value)
                ? prevSelectedSprints.filter((sprint) => sprint !== value) // Deselecting
                : [...prevSelectedSprints, value] // Selecting
        );
    };

    // Handle the generation button click
    const handleGenerate = async () => {
        if (selectedSprints.length === 0) {
            alert('Please select at least one sprint.');
            return;
        }

        setLoading(true);

        try {
            const response = await axios.post('/generate/', { sprints: selectedSprints }, {
                responseType: 'blob', // Ensure the response is a binary file
            });

            // Create a URL for the Word document and set it for downloading
            const url = window.URL.createObjectURL(new Blob([response.data], { type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' }));
            setDocUrl(url);
        } catch (error) {
            console.error('Error generating release notes:', error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <h1>Release Notes Generator</h1>

            {/* Sprint Selection - Checklist */}
            <div>
                <h3>Select Sprints</h3>
                {sprints.length > 0 ? (
                    <div>
                        {/* Render a checklist for selecting multiple sprints */}
                        <ul style={{ listStyleType: 'none', padding: 0 }}>
                            {sprints.map((sprint) => (
                                <li key={sprint.name} style={{ margin: '10px 0' }}>
                                    <label>
                                        <input
                                            type="checkbox"
                                            value={sprint.name}
                                            onChange={handleSprintChange}
                                            checked={selectedSprints.includes(sprint.name)} // Mark the checkbox if selected
                                        />
                                        {sprint.name}
                                    </label>
                                </li>
                            ))}
                        </ul>
                    </div>
                ) : (
                    <p>Loading sprints...</p>
                )}
            </div>

            {/* Generate Button */}
            <div>
                <button onClick={handleGenerate} disabled={loading}>
                    {loading ? 'Generating...' : 'Generate'}
                </button>
            </div>

            {/* Spinner */}
            {loading && <div className="spinner"></div>}

            {/* Document Download */}
            {docUrl && (
                <div>
                    <h3>Release Notes Generated</h3>
                    <a href={docUrl} download="release_notes.docx">
                        Download Word Document
                    </a>
                </div>
            )}
        </div>
    );
};

export default ReleaseNotesGenerator;
