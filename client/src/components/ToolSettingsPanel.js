import React, { useState } from 'react';
import { downloadJournals, processMarkdown, downloadPdfs, pdfToAudio } from '../services/api';

export default function ToolSettingsPanel() {
  // Journals
  const [journalQuery, setJournalQuery] = useState('');
  const [journalLoading, setJournalLoading] = useState(false);
  const [journalResult, setJournalResult] = useState(null);
  const [journalError, setJournalError] = useState('');

  // Markdown
  const [markdownFile, setMarkdownFile] = useState('');
  const [markdownLoading, setMarkdownLoading] = useState(false);
  const [markdownResult, setMarkdownResult] = useState(null);
  const [markdownError, setMarkdownError] = useState('');

  // PDFs
  const [pdfQuery, setPdfQuery] = useState('');
  const [pdfMax, setPdfMax] = useState(5);
  const [pdfLoading, setPdfLoading] = useState(false);
  const [pdfResult, setPdfResult] = useState(null);
  const [pdfError, setPdfError] = useState('');

  // PDF to Audio
  const [pdfFile, setPdfFile] = useState('');
  const [audioLoading, setAudioLoading] = useState(false);
  const [audioResult, setAudioResult] = useState(null);
  const [audioError, setAudioError] = useState('');

  // File picker for markdown/pdf
  const handleFilePick = (setter) => (e) => {
    if (e.target.files && e.target.files[0]) {
      setter(e.target.files[0].path || e.target.files[0].name);
    }
  };

  return (
    <div className="tool-settings-panel">
      <h2>Tool Settings</h2>

      {/* Download Journals */}
      <div>
        <h3>Download Journals</h3>
        <input
          value={journalQuery}
          onChange={e => setJournalQuery(e.target.value)}
          placeholder="Journal search query"
        />
        <button
          onClick={async () => {
            setJournalLoading(true); setJournalError(''); setJournalResult(null);
            try {
              const res = await downloadJournals(journalQuery);
              setJournalResult(res.data);
            } catch (e) {
              setJournalError(e.message);
            } finally {
              setJournalLoading(false);
            }
          }}
          disabled={!journalQuery || journalLoading}
        >{journalLoading ? 'Loading...' : 'Run'}</button>
        {journalError && <div style={{ color: 'red' }}>{journalError}</div>}
        {journalResult && (
          <div style={{ maxHeight: 200, overflow: 'auto' }}>
            <table>
              <thead>
                <tr>
                  <th>Title</th><th>Abstract</th>
                </tr>
              </thead>
              <tbody>
                {journalResult.records?.slice(0, 10).map((rec, i) => (
                  <tr key={i}>
                    <td>{rec.title}</td>
                    <td>{rec.abstract?.slice(0, 100)}...</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Process Markdown */}
      <div>
        <h3>Process Markdown</h3>
        <input
          type="text"
          value={markdownFile}
          onChange={e => setMarkdownFile(e.target.value)}
          placeholder="Path to markdown file"
        />
        <input type="file" style={{ marginLeft: 8 }} onChange={handleFilePick(setMarkdownFile)} />
        <button
          onClick={async () => {
            setMarkdownLoading(true); setMarkdownError(''); setMarkdownResult(null);
            try {
              const res = await processMarkdown(markdownFile);
              setMarkdownResult(res.data);
            } catch (e) {
              setMarkdownError(e.message);
            } finally {
              setMarkdownLoading(false);
            }
          }}
          disabled={!markdownFile || markdownLoading}
        >{markdownLoading ? 'Processing...' : 'Run'}</button>
        {markdownError && <div style={{ color: 'red' }}>{markdownError}</div>}
        {markdownResult && (
          <div>
            <strong>Slides:</strong>
            <ul>
              {markdownResult.slide_titles?.map((title, i) => <li key={i}>{title}</li>)}
            </ul>
          </div>
        )}
      </div>

      {/* Download PDFs */}
      <div>
        <h3>Download PDFs</h3>
        <input
          value={pdfQuery}
          onChange={e => setPdfQuery(e.target.value)}
          placeholder="PDF search query"
        />
        <input
          type="number"
          min={1}
          max={50}
          value={pdfMax}
          onChange={e => setPdfMax(Number(e.target.value))}
          style={{ width: 60, marginLeft: 8 }}
          placeholder="Max"
        />
        <span style={{ marginLeft: 4 }}># to download</span>
        <button
          onClick={async () => {
            setPdfLoading(true); setPdfError(''); setPdfResult(null);
            try {
              const res = await downloadPdfs([pdfQuery], pdfMax);
              setPdfResult(res.data);
            } catch (e) {
              setPdfError(e.message);
            } finally {
              setPdfLoading(false);
            }
          }}
          disabled={!pdfQuery || pdfLoading}
        >{pdfLoading ? 'Downloading...' : 'Run'}</button>
        {pdfError && <div style={{ color: 'red' }}>{pdfError}</div>}
        {pdfResult && (
          <div>
            <strong>Files:</strong>
            <ul>
              {pdfResult.files?.map((f, i) => <li key={i}>{f}</li>)}
            </ul>
            {pdfResult.errors?.length > 0 && (
              <div style={{ color: 'red' }}>
                <strong>Errors:</strong>
                <ul>{pdfResult.errors.map((err, i) => <li key={i}>{err}</li>)}</ul>
              </div>
            )}
          </div>
        )}
      </div>

      {/* PDF to Audio */}
      <div>
        <h3>PDF to Audio</h3>
        <input
          type="text"
          value={pdfFile}
          onChange={e => setPdfFile(e.target.value)}
          placeholder="Path to PDF file"
        />
        <input type="file" style={{ marginLeft: 8 }} onChange={handleFilePick(setPdfFile)} />
        <button
          onClick={async () => {
            setAudioLoading(true); setAudioError(''); setAudioResult(null);
            try {
              const res = await pdfToAudio(pdfFile);
              setAudioResult(res.data);
            } catch (e) {
              setAudioError(e.message);
            } finally {
              setAudioLoading(false);
            }
          }}
          disabled={!pdfFile || audioLoading}
        >{audioLoading ? 'Converting...' : 'Run'}</button>
        {audioError && <div style={{ color: 'red' }}>{audioError}</div>}
        {audioResult && (
          <div>
            <strong>Audio Files:</strong>
            <ul>
              {audioResult.files?.map((f, i) => <li key={i}>{f}</li>)}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
} 