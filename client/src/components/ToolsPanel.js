import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  TextField,
  Button,
  Grid,
  Alert,
  CircularProgress,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  List,
  ListItem,
  ListItemText,
  Chip,
  Divider
} from '@mui/material';
import {
  Search as SearchIcon,
  Download as DownloadIcon,
  VolumeUp as AudioIcon,
  Description as MarkdownIcon,
  School as JournalIcon,
  ExpandMore as ExpandMoreIcon,
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon
} from '@mui/icons-material';
import {
  searchAndDownloadPDFs,
  convertPDFToAudio,
  processMarkdown,
  fetchJournals,
  openJournals
} from '../services/toolsApi';
import './ToolsPanel.css';

const ToolsPanel = () => {
  const [loading, setLoading] = useState({});
  const [results, setResults] = useState({});
  const [errors, setErrors] = useState({});
  const [inputs, setInputs] = useState({
    searchQuery: '',
    pdfFile: '',
    markdownContent: '',
    journalQuery: ''
  });

  const handleInputChange = (field, value) => {
    setInputs(prev => ({ ...prev, [field]: value }));
    // Clear previous results/errors when input changes
    setResults(prev => ({ ...prev, [field]: null }));
    setErrors(prev => ({ ...prev, [field]: null }));
  };

  const handleToolAction = async (toolName, action) => {
    setLoading(prev => ({ ...prev, [toolName]: true }));
    setErrors(prev => ({ ...prev, [toolName]: null }));
    setResults(prev => ({ ...prev, [toolName]: null }));

    try {
      let response;
      switch (toolName) {
        case 'searchDownload':
          response = await searchAndDownloadPDFs(inputs.searchQuery);
          break;
        case 'pdfToAudio':
          response = await convertPDFToAudio(inputs.pdfFile);
          break;
        case 'markdown':
          response = await processMarkdown(inputs.markdownContent);
          break;
        case 'fetchJournals':
          response = await fetchJournals(inputs.journalQuery);
          break;
        case 'openJournals':
          response = await openJournals(inputs.journalQuery);
          break;
        default:
          throw new Error('Unknown tool');
      }

      setResults(prev => ({ ...prev, [toolName]: response.data }));
    } catch (error) {
      console.error(`Error in ${toolName}:`, error);
      setErrors(prev => ({ 
        ...prev, 
        [toolName]: error.response?.data?.error || error.message || 'An error occurred'
      }));
    } finally {
      setLoading(prev => ({ ...prev, [toolName]: false }));
    }
  };

  const renderSearchDownloadTool = () => (
    <Accordion>
      <AccordionSummary expandIcon={<ExpandMoreIcon />}>
        <SearchIcon sx={{ mr: 1 }} />
        <Typography variant="h6">Search & Download PDFs</Typography>
      </AccordionSummary>
      <AccordionDetails>
        <Box sx={{ mb: 2 }}>
          <TextField
            fullWidth
            label="Search Query"
            value={inputs.searchQuery}
            onChange={(e) => handleInputChange('searchQuery', e.target.value)}
            placeholder="e.g., machine learning textbooks filetype:pdf"
            helperText="Enter a search query to find and download PDFs"
          />
        </Box>
        <Button
          variant="contained"
          onClick={() => handleToolAction('searchDownload')}
          disabled={loading.searchDownload || !inputs.searchQuery.trim()}
          startIcon={loading.searchDownload ? <CircularProgress size={20} /> : <DownloadIcon />}
        >
          {loading.searchDownload ? 'Searching...' : 'Search & Download'}
        </Button>
        
        {results.searchDownload && (
          <Box sx={{ mt: 2 }}>
            <Alert severity="success" icon={<CheckCircleIcon />}>
              {results.searchDownload.message}
            </Alert>
            {results.searchDownload.files && results.searchDownload.files.length > 0 && (
              <List dense>
                {results.searchDownload.files.map((file, index) => (
                  <ListItem key={index}>
                    <ListItemText primary={file} />
                    <Chip label="Downloaded" color="success" size="small" />
                  </ListItem>
                ))}
              </List>
            )}
          </Box>
        )}
        
        {errors.searchDownload && (
          <Alert severity="error" icon={<ErrorIcon />} sx={{ mt: 2 }}>
            {errors.searchDownload}
          </Alert>
        )}
      </AccordionDetails>
    </Accordion>
  );

  const renderPDFToAudioTool = () => (
    <Accordion>
      <AccordionSummary expandIcon={<ExpandMoreIcon />}>
        <AudioIcon sx={{ mr: 1 }} />
        <Typography variant="h6">Convert PDF to Audio</Typography>
      </AccordionSummary>
      <AccordionDetails>
        <Box sx={{ mb: 2 }}>
          <TextField
            fullWidth
            label="PDF File Path"
            value={inputs.pdfFile}
            onChange={(e) => handleInputChange('pdfFile', e.target.value)}
            placeholder="e.g., /path/to/document.pdf"
            helperText="Enter the full path to the PDF file on the server"
          />
        </Box>
        <Button
          variant="contained"
          onClick={() => handleToolAction('pdfToAudio')}
          disabled={loading.pdfToAudio || !inputs.pdfFile.trim()}
          startIcon={loading.pdfToAudio ? <CircularProgress size={20} /> : <AudioIcon />}
        >
          {loading.pdfToAudio ? 'Converting...' : 'Convert to Audio'}
        </Button>
        
        {results.pdfToAudio && (
          <Box sx={{ mt: 2 }}>
            <Alert severity="success" icon={<CheckCircleIcon />}>
              {results.pdfToAudio.message}
            </Alert>
            {results.pdfToAudio.audio_files && results.pdfToAudio.audio_files.length > 0 && (
              <List dense>
                {results.pdfToAudio.audio_files.map((file, index) => (
                  <ListItem key={index}>
                    <ListItemText primary={file} />
                    <Chip label="Generated" color="success" size="small" />
                  </ListItem>
                ))}
              </List>
            )}
          </Box>
        )}
        
        {errors.pdfToAudio && (
          <Alert severity="error" icon={<ErrorIcon />} sx={{ mt: 2 }}>
            {errors.pdfToAudio}
          </Alert>
        )}
      </AccordionDetails>
    </Accordion>
  );

  const renderMarkdownTool = () => (
    <Accordion>
      <AccordionSummary expandIcon={<ExpandMoreIcon />}>
        <MarkdownIcon sx={{ mr: 1 }} />
        <Typography variant="h6">Process Markdown to Presentations</Typography>
      </AccordionSummary>
      <AccordionDetails>
        <Box sx={{ mb: 2 }}>
          <TextField
            fullWidth
            multiline
            rows={6}
            label="Markdown Content"
            value={inputs.markdownContent}
            onChange={(e) => handleInputChange('markdownContent', e.target.value)}
            placeholder="### Slide 1:&#10;**Slide Text Content:** Introduction to AI&#10;**Image Prompt:** AI robot&#10;---&#10;### Slide 2:&#10;**Slide Text Content:** Machine Learning Basics&#10;**Image Prompt:** Neural network diagram"
            helperText="Enter markdown content in the specified format for slides"
          />
        </Box>
        <Button
          variant="contained"
          onClick={() => handleToolAction('markdown')}
          disabled={loading.markdown || !inputs.markdownContent.trim()}
          startIcon={loading.markdown ? <CircularProgress size={20} /> : <MarkdownIcon />}
        >
          {loading.markdown ? 'Processing...' : 'Generate Presentation'}
        </Button>
        
        {results.markdown && (
          <Box sx={{ mt: 2 }}>
            <Alert severity="success" icon={<CheckCircleIcon />}>
              {results.markdown.message}
            </Alert>
            {results.markdown.files && results.markdown.files.length > 0 && (
              <List dense>
                {results.markdown.files.map((file, index) => (
                  <ListItem key={index}>
                    <ListItemText primary={file} />
                    <Chip label="Generated" color="success" size="small" />
                  </ListItem>
                ))}
              </List>
            )}
          </Box>
        )}
        
        {errors.markdown && (
          <Alert severity="error" icon={<ErrorIcon />} sx={{ mt: 2 }}>
            {errors.markdown}
          </Alert>
        )}
      </AccordionDetails>
    </Accordion>
  );

  const renderJournalTools = () => (
    <>
      <Accordion>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <JournalIcon sx={{ mr: 1 }} />
          <Typography variant="h6">Fetch Academic Journals</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Box sx={{ mb: 2 }}>
            <TextField
              fullWidth
              label="Journal Query"
              value={inputs.journalQuery}
              onChange={(e) => handleInputChange('journalQuery', e.target.value)}
              placeholder="e.g., deep learning neural networks"
              helperText="Search for academic papers using OpenAlex and Google Scholar"
            />
          </Box>
          <Button
            variant="contained"
            onClick={() => handleToolAction('fetchJournals')}
            disabled={loading.fetchJournals || !inputs.journalQuery.trim()}
            startIcon={loading.fetchJournals ? <CircularProgress size={20} /> : <SearchIcon />}
          >
            {loading.fetchJournals ? 'Fetching...' : 'Fetch Journals'}
          </Button>
          
          {results.fetchJournals && (
            <Box sx={{ mt: 2 }}>
              <Alert severity="success" icon={<CheckCircleIcon />}>
                {results.fetchJournals.message}
              </Alert>
              <Typography variant="body2" sx={{ mt: 1 }}>
                Found {JSON.parse(results.fetchJournals.data).length} papers
              </Typography>
            </Box>
          )}
          
          {errors.fetchJournals && (
            <Alert severity="error" icon={<ErrorIcon />} sx={{ mt: 2 }}>
              {errors.fetchJournals}
            </Alert>
          )}
        </AccordionDetails>
      </Accordion>

      <Accordion>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <DownloadIcon sx={{ mr: 1 }} />
          <Typography variant="h6">Open & Download Academic Papers</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Box sx={{ mb: 2 }}>
            <TextField
              fullWidth
              label="Paper Query"
              value={inputs.journalQuery}
              onChange={(e) => handleInputChange('journalQuery', e.target.value)}
              placeholder="e.g., machine learning applications"
              helperText="Search and download academic papers using CORE API"
            />
          </Box>
          <Button
            variant="contained"
            onClick={() => handleToolAction('openJournals')}
            disabled={loading.openJournals || !inputs.journalQuery.trim()}
            startIcon={loading.openJournals ? <CircularProgress size={20} /> : <DownloadIcon />}
          >
            {loading.openJournals ? 'Downloading...' : 'Open & Download Papers'}
          </Button>
          
          {results.openJournals && (
            <Box sx={{ mt: 2 }}>
              <Alert severity="success" icon={<CheckCircleIcon />}>
                {results.openJournals.message}
              </Alert>
              <Typography variant="body2" sx={{ mt: 1 }}>
                Found {JSON.parse(results.openJournals.data).length} papers
              </Typography>
            </Box>
          )}
          
          {errors.openJournals && (
            <Alert severity="error" icon={<ErrorIcon />} sx={{ mt: 2 }}>
              {errors.openJournals}
            </Alert>
          )}
        </AccordionDetails>
      </Accordion>
    </>
  );

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        AI Tools Panel
      </Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
        Access powerful AI tools for document processing, research, and content creation.
      </Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          {renderSearchDownloadTool()}
        </Grid>
        <Grid item xs={12} md={6}>
          {renderPDFToAudioTool()}
        </Grid>
        <Grid item xs={12}>
          {renderMarkdownTool()}
        </Grid>
        <Grid item xs={12}>
          {renderJournalTools()}
        </Grid>
      </Grid>
    </Box>
  );
};

export default ToolsPanel; 