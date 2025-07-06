# AI Core Service API Documentation

## Base URL
```
http://localhost:5003
```

## Health Check
### GET /health
Check if the service is running and all components are healthy.

**Response:**
```json
{
  "status": "ok",
  "embedding_model_type": "sentence-transformers",
  "embedding_model_name": "all-MiniLM-L6-v2",
  "embedding_dimension": 384,
  "sentence_transformer_load": "OK",
  "default_index_loaded": true,
  "gemini_sdk_installed": true,
  "ollama_available": true,
  "groq_sdk_installed": true,
  "message": "AI Core service is running. Embeddings OK."
}
```

## New Tool Endpoints

### 1. Search and Download PDFs
**POST /search_and_download**

Search for PDFs online and download them based on a query.

**Request Body:**
```json
{
  "query": "machine learning textbooks filetype:pdf"
}
```

**Response:**
```json
{
  "message": "Search and download completed",
  "files": ["pdf_1.pdf", "arxiv_1234.5678.pdf"],
  "status": "success"
}
```

**Error Response:**
```json
{
  "error": "Search_download module not found",
  "status": "error"
}
```

---

### 2. Convert PDF to Audio
**POST /convert_pdf_to_audio**

Convert a PDF file to audio files using text-to-speech.

**Request Body:**
```json
{
  "pdf_file": "/path/to/document.pdf"
}
```

**Response:**
```json
{
  "message": "Audio conversion completed for /path/to/document.pdf",
  "audio_files": ["document_part1.mp3", "document_part2.mp3"],
  "status": "success"
}
```

**Error Response:**
```json
{
  "error": "PDF file not found: /path/to/document.pdf",
  "status": "error"
}
```

---

### 3. Process Markdown to Presentations
**POST /process_markdown**

Convert markdown content to PowerPoint presentation and Word documents.

**Request Body:**
```json
{
  "markdown_content": "### Slide 1:\n**Slide Text Content:** Introduction to AI\n**Image Prompt:** AI robot\n---\n### Slide 2:\n**Slide Text Content:** Machine Learning Basics\n**Image Prompt:** Neural network diagram"
}
```

**Response:**
```json
{
  "message": "Markdown processed and files generated",
  "files": ["output/Presentation.pptx", "output/ImagePrompt.DOC", "output/OtherNotes.DOC"],
  "status": "success"
}
```

**Error Response:**
```json
{
  "error": "Missing 'markdown_content' parameter",
  "status": "error"
}
```

---

### 4. Fetch Academic Journals
**POST /fetch_journals**

Search for academic papers using OpenAlex and Google Scholar.

**Request Body:**
```json
{
  "query": "deep learning neural networks"
}
```

**Response:**
```json
{
  "message": "Journals fetched",
  "data": "[{\"title\":\"Deep Learning for Neural Networks\",\"abstract\":\"...\",\"year\":\"2023\",\"citations\":150}]",
  "status": "success"
}
```

**Error Response:**
```json
{
  "error": "_1journal_fetch module not found",
  "status": "error"
}
```

---

### 5. Open and Download Academic Papers
**POST /open_journals**

Search and download academic papers using CORE API.

**Request Body:**
```json
{
  "query": "machine learning applications"
}
```

**Response:**
```json
{
  "message": "Journals opened",
  "data": "[{\"title\":\"ML Applications\",\"abstract\":\"...\",\"download_url\":\"https://...\",\"filename\":\"core_downloads/1_0_ML_Applications.pdf\"}]",
  "status": "success"
}
```

**Error Response:**
```json
{
  "error": "_1journal_open module not found",
  "status": "error"
}
```

---

## Frontend Integration Examples

### JavaScript/TypeScript Examples

#### 1. Search and Download PDFs
```javascript
async function searchAndDownloadPDFs(query) {
  try {
    const response = await fetch('http://localhost:5003/search_and_download', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query })
    });
    
    const result = await response.json();
    if (result.status === 'success') {
      console.log('Downloaded files:', result.files);
      return result.files;
    } else {
      throw new Error(result.error);
    }
  } catch (error) {
    console.error('Error:', error);
    throw error;
  }
}
```

#### 2. Convert PDF to Audio
```javascript
async function convertPDFToAudio(pdfFilePath) {
  try {
    const response = await fetch('http://localhost:5003/convert_pdf_to_audio', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ pdf_file: pdfFilePath })
    });
    
    const result = await response.json();
    if (result.status === 'success') {
      console.log('Audio files:', result.audio_files);
      return result.audio_files;
    } else {
      throw new Error(result.error);
    }
  } catch (error) {
    console.error('Error:', error);
    throw error;
  }
}
```

#### 3. Process Markdown
```javascript
async function processMarkdown(markdownContent) {
  try {
    const response = await fetch('http://localhost:5003/process_markdown', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ markdown_content: markdownContent })
    });
    
    const result = await response.json();
    if (result.status === 'success') {
      console.log('Generated files:', result.files);
      return result.files;
    } else {
      throw new Error(result.error);
    }
  } catch (error) {
    console.error('Error:', error);
    throw error;
  }
}
```

#### 4. Fetch Journals
```javascript
async function fetchJournals(query) {
  try {
    const response = await fetch('http://localhost:5003/fetch_journals', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query })
    });
    
    const result = await response.json();
    if (result.status === 'success') {
      const journals = JSON.parse(result.data);
      console.log('Journals:', journals);
      return journals;
    } else {
      throw new Error(result.error);
    }
  } catch (error) {
    console.error('Error:', error);
    throw error;
  }
}
```

#### 5. Open Journals
```javascript
async function openJournals(query) {
  try {
    const response = await fetch('http://localhost:5003/open_journals', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query })
    });
    
    const result = await response.json();
    if (result.status === 'success') {
      const papers = JSON.parse(result.data);
      console.log('Papers:', papers);
      return papers;
    } else {
      throw new Error(result.error);
    }
  } catch (error) {
    console.error('Error:', error);
    throw error;
  }
}
```

## Error Handling

All endpoints return consistent error responses:

```json
{
  "error": "Error description",
  "status": "error"
}
```

Common HTTP status codes:
- `200`: Success
- `400`: Bad Request (missing parameters)
- `404`: Not Found (file not found)
- `500`: Internal Server Error (module not found, processing error)

## Notes

1. **File Paths**: Ensure PDF files exist on the server before calling `/convert_pdf_to_audio`
2. **Output Directory**: Generated files are saved in the `output/` directory
3. **API Keys**: Some tools require API keys (Gemini, CORE) - ensure they are configured
4. **Rate Limits**: Journal fetching tools respect API rate limits
5. **File Formats**: 
   - PDF to Audio: Generates MP3 files
   - Markdown: Generates PPTX and DOC files
   - Journals: Downloads PDF files

## Testing

You can test the endpoints using curl:

```bash
# Health check
curl http://localhost:5003/health

# Search and download
curl -X POST http://localhost:5003/search_and_download \
  -H "Content-Type: application/json" \
  -d '{"query": "machine learning"}'

# Convert PDF to audio
curl -X POST http://localhost:5003/convert_pdf_to_audio \
  -H "Content-Type: application/json" \
  -d '{"pdf_file": "/path/to/file.pdf"}'
``` 