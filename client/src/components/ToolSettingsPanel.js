import React, { useState } from 'react';
import './ToolSettingsPanel.css';

const ToolSettingsPanel = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [pdfFile, setPdfFile] = useState('');
  const [markdownContent, setMarkdownContent] = useState('');
  const [journalQuery, setJournalQuery] = useState('');
  const [resultMessage, setResultMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSearchAndDownload = async () => {
    setIsLoading(true);
    setResultMessage('');
    try {
      const response = await fetch('/search_and_download', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: searchQuery }),
      });
      const data = await response.json();
      if (response.ok) {
        setResultMessage(`Downloaded files: ${data.files.join(', ')}`);
      } else {
        setResultMessage(`Error: ${data.error}`);
      }
    } catch (error) {
      setResultMessage(`Error: ${error.message}`);
    }
    setIsLoading(false);
  };

  const handleConvertPdfToAudio = async () => {
    setIsLoading(true);
    setResultMessage('');
    try {
      const response = await fetch('/convert_pdf_to_audio', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ pdf_file: pdfFile }),
      });
      const data = await response.json();
      if (response.ok) {
        setResultMessage(data.message);
      } else {
        setResultMessage(`Error: ${data.error}`);
      }
    } catch (error) {
      setResultMessage(`Error: ${error.message}`);
    }
    setIsLoading(false);
  };

  const handleProcessMarkdown = async () => {
    setIsLoading(true);
    setResultMessage('');
    try {
      const response = await fetch('/process_markdown', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ markdown_content: markdownContent }),
      });
      const data = await response.json();
      if (response.ok) {
        setResultMessage(data.message);
      } else {
        setResultMessage(`Error: ${data.error}`);
      }
    } catch (error) {
      setResultMessage(`Error: ${error.message}`);
    }
    setIsLoading(false);
  };

  const handleFetchJournals = async () => {
    setIsLoading(true);
    setResultMessage('');
    try {
      const response = await fetch('/fetch_journals', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: journalQuery }),
      });
      const data = await response.json();
      if (response.ok) {
        setResultMessage(`Fetched journals: ${data.data.length} records`);
      } else {
        setResultMessage(`Error: ${data.error}`);
      }
    } catch (error) {
      setResultMessage(`Error: ${error.message}`);
    }
    setIsLoading(false);
  };

  const handleOpenJournals = async () => {
    setIsLoading(true);
    setResultMessage('');
    try {
      const response = await fetch('/open_journals', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: journalQuery }),
      });
      const data = await response.json();
      if (response.ok) {
        setResultMessage(`Opened journals: ${data.data.length} records`);
      } else {
        setResultMessage(`Error: ${data.error}`);
      }
    } catch (error) {
      setResultMessage(`Error: ${error.message}`);
    }
    setIsLoading(false);
  };

  return (
    <div className="tool-settings-panel">
      <h3>Tool Settings</h3>

      <div className="tool-section">
        <h4>Search and Download PDFs</h4>
        <input
          type="text"
          placeholder="Enter search query"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          disabled={isLoading}
        />
        <button onClick={handleSearchAndDownload} disabled={isLoading || !searchQuery}>
          Search & Download
        </button>
      </div>

      <div className="tool-section">
        <h4>Convert PDF to Audio</h4>
        <input
          type="text"
          placeholder="Enter PDF file path"
          value={pdfFile}
          onChange={(e) => setPdfFile(e.target.value)}
          disabled={isLoading}
        />
        <button onClick={handleConvertPdfToAudio} disabled={isLoading || !pdfFile}>
          Convert to Audio
        </button>
      </div>

      <div className="tool-section">
        <h4>Process Markdown</h4>
        <textarea
          placeholder="Enter markdown content"
          value={markdownContent}
          onChange={(e) => setMarkdownContent(e.target.value)}
          disabled={isLoading}
          rows={6}
        />
        <button onClick={handleProcessMarkdown} disabled={isLoading || !markdownContent}>
          Process Markdown
        </button>
      </div>

      <div className="tool-section">
        <h4>Fetch Journals</h4>
        <input
          type="text"
          placeholder="Enter journal search query"
          value={journalQuery}
          onChange={(e) => setJournalQuery(e.target.value)}
          disabled={isLoading}
        />
        <button onClick={handleFetchJournals} disabled={isLoading || !journalQuery}>
          Fetch Journals
        </button>
      </div>

      <div className="tool-section">
        <h4>Open Journals</h4>
        <input
          type="text"
          placeholder="Enter journal open query"
          value={journalQuery}
          onChange={(e) => setJournalQuery(e.target.value)}
          disabled={isLoading}
        />
        <button onClick={handleOpenJournals} disabled={isLoading || !journalQuery}>
          Open Journals
        </button>
      </div>

      {resultMessage && <div className="result-message">{resultMessage}</div>}
    </div>
  );
};

export default ToolSettingsPanel;
