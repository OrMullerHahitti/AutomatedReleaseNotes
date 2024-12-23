import logo from './logo.svg';
import React, { useState } from 'react';
import './App.css';
 
function App() {
  // State for sprint data, loading, error, selected sprints
  const [sprints, setSprints] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedSprints, setSelectedSprints] = useState([]); // Track selected sprints for release notes
 
  // Fetch sprints when "List Sprints" is clicked
  const fetchSprints = async () => {
    setLoading(true);
    setError(null);
    setSelectedSprints([]); // Reset selected sprints when fetching new data
 
    const apiUrl = 'https://example.com/api/sprints'; // Replace with actual API URL
    try {
      const response = await fetch(apiUrl);
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      setSprints(data);
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };
 
  // Handle checkbox change to track selected sprints
  const handleCheckboxChange = (event, sprintDate) => {
    if (event.target.checked) {
      setSelectedSprints((prev) => [...prev, sprintDate]); // Add selected sprint date
    } else {
      setSelectedSprints((prev) => prev.filter((date) => date !== sprintDate)); // Remove unselected sprint date
    }
  };
 
  // Make release notes API call with selected sprint dates
  const makeReleaseNotes = async () => {
    if (selectedSprints.length === 0) {
      alert('Please select at least one sprint.');
      return;
    }
 
    setLoading(true);
    setError(null);
 
    const apiUrl = 'https://example.com/api/release-notes'; // Replace with actual API URL
    try {
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ sprintDates: selectedSprints }), // Pass the selected sprint dates
      });
      if (!response.ok) {
        throw new Error('Error generating release notes');
      }
      const blob = await response.blob(); // Get the Word file from the response
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = 'release_notes.docx'; // Set the file name for download
      link.click(); // Trigger the download
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };
 
  return (
    <div className="App">
      <header className="App-header">
        <h1>Sprints List</h1>
 
        <button onClick={fetchSprints} disabled={loading}>
          {loading ? 'Loading...' : 'List Sprints'}
        </button>
 
        {error && <p>Error: {error}</p>}
 
        {sprints.length > 0 && !loading && (
          <div>
            <h2>Select Sprints for Release Notes</h2>
            <ul>
              {sprints.map((sprint, index) => (
                <li key={index}>
                  <label>
                    <input
                      type="checkbox"
                      value={sprint.startDate}
                      onChange={(event) => handleCheckboxChange(event, sprint.startDate)}
                    />
                    <strong>{sprint.name}</strong> - {sprint.startDate} to {sprint.endDate}
                  </label>
                </li>
              ))}
            </ul>
 
            <button onClick={makeReleaseNotes} disabled={loading || selectedSprints.length === 0}>
              {loading ? 'Processing...' : 'Make Release Notes'}
            </button>
          </div>
        )}
      </header>
    </div>
  );
}
 
export default App;
 
 
  /*
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
  */