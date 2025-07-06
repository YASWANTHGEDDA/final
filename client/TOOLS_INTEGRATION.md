# AI Tools Integration

## Overview
The frontend now includes a comprehensive AI Tools panel that provides access to powerful backend tools for document processing, research, and content creation.

## Accessing the Tools

### Method 1: Via Chat Interface
1. Open the chat interface
2. Click the **Tools** button (🔧) in the header
3. The Tools panel will appear in the sidebar

### Method 2: Direct URL
Navigate to `/tools` in your browser (requires authentication)

## Available Tools

### 1. Search & Download PDFs
- **Purpose**: Search the web for PDFs and download them automatically
- **Input**: Search query (e.g., "machine learning textbooks filetype:pdf")
- **Output**: List of downloaded PDF files
- **Features**: 
  - Uses DuckDuckGo search
  - Filters results using AI
  - Downloads arXiv papers and other PDFs

### 2. Convert PDF to Audio
- **Purpose**: Convert PDF documents to audio files using text-to-speech
- **Input**: Full path to PDF file on the server
- **Output**: MP3 audio files (split into chunks)
- **Features**:
  - Configurable chunk duration
  - Overlap between chunks for smooth listening
  - Uses Google Text-to-Speech

### 3. Process Markdown to Presentations
- **Purpose**: Convert markdown content to PowerPoint presentations and Word documents
- **Input**: Markdown content in specific format
- **Output**: PPTX and DOC files
- **Features**:
  - Generates PowerPoint presentations
  - Creates Word documents for image prompts and author notes
  - Supports markdown formatting

### 4. Fetch Academic Journals
- **Purpose**: Search for academic papers using OpenAlex and Google Scholar
- **Input**: Research query
- **Output**: List of academic papers with metadata
- **Features**:
  - Searches multiple academic databases
  - Returns title, abstract, year, citations
  - Filters by publication type

### 5. Open & Download Academic Papers
- **Purpose**: Search and download academic papers using CORE API
- **Input**: Research query
- **Output**: Downloaded PDF files and metadata
- **Features**:
  - Downloads full papers when available
  - Respects API rate limits
  - Returns comprehensive metadata

## Technical Implementation

### Backend Integration
- **API Base URL**: `http://localhost:5003` (configurable via `REACT_APP_BACKEND_PORT`)
- **Separate API Service**: `toolsApi.js` for direct backend communication
- **Error Handling**: Comprehensive error handling with user-friendly messages
- **Loading States**: Visual feedback during tool execution

### Frontend Components
- **ToolsPanel.js**: Main component with accordion-style interface
- **ToolsPanel.css**: Styling for responsive design
- **toolsApi.js**: API service for backend communication

### API Endpoints
- `POST /search_and_download` - Search and download PDFs
- `POST /convert_pdf_to_audio` - Convert PDF to audio
- `POST /process_markdown` - Process markdown to presentations
- `POST /fetch_journals` - Fetch academic journals
- `POST /open_journals` - Open and download academic papers
- `GET /health` - Health check for tools backend

## Usage Examples

### Search and Download PDFs
```javascript
// Example query
"machine learning textbooks filetype:pdf"

// Response
{
  "message": "Search and download completed",
  "files": ["pdf_1.pdf", "arxiv_1234.5678.pdf"],
  "status": "success"
}
```

### Convert PDF to Audio
```javascript
// Example input
"/path/to/document.pdf"

// Response
{
  "message": "Audio conversion completed for /path/to/document.pdf",
  "audio_files": ["document_part1.mp3", "document_part2.mp3"],
  "status": "success"
}
```

### Process Markdown
```javascript
// Example input
"### Slide 1:\n**Slide Text Content:** Introduction to AI\n**Image Prompt:** AI robot"

// Response
{
  "message": "Markdown processed and files generated",
  "files": ["output/Presentation.pptx", "output/ImagePrompt.DOC"],
  "status": "success"
}
```

## Error Handling

The tools panel provides comprehensive error handling:

- **Input Validation**: Checks for required fields
- **File Existence**: Validates file paths before processing
- **API Errors**: Displays backend error messages
- **Network Issues**: Handles connection problems gracefully
- **Loading States**: Shows progress during tool execution

## Configuration

### Environment Variables
- `REACT_APP_BACKEND_PORT`: Backend port (default: 5003)

### Backend Requirements
Ensure the backend has all required dependencies installed:
```bash
pip install -r requirements.txt
```

### API Keys
Some tools require API keys:
- **Gemini API**: For search filtering
- **CORE API**: For academic paper downloads

## Troubleshooting

### Common Issues

1. **"Module not found" errors**
   - Ensure all backend dependencies are installed
   - Check that the backend is running on the correct port

2. **"File not found" errors**
   - Verify file paths are correct
   - Ensure files exist on the server

3. **"API key" errors**
   - Configure required API keys in the backend
   - Check API key validity

4. **Network errors**
   - Verify backend is running
   - Check CORS configuration
   - Ensure correct port configuration

### Debug Mode
Enable debug logging in the browser console to see detailed API calls and responses.

## Future Enhancements

- File upload interface for PDF conversion
- Real-time progress indicators
- Batch processing capabilities
- Integration with existing file management system
- Export results to various formats
- Custom tool configurations 