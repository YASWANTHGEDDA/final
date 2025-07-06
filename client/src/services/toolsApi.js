// client/src/services/toolsApi.js
import axios from 'axios';

// Dynamically determine API Base URL for tools (Node.js backend proxy)
const getToolsApiBaseUrl = () => {
    const backendPort = process.env.REACT_APP_BACKEND_PORT || 5003;
    const hostname = window.location.hostname;
    const protocol = window.location.protocol === 'https:' ? 'https:' : 'http:';
    const backendHost = (hostname === 'localhost' || hostname === '127.0.0.1') ? 'localhost' : hostname;
    return `${protocol}//${backendHost}:${backendPort}`;
};

const TOOLS_API_BASE_URL = getToolsApiBaseUrl();
const toolsApi = axios.create({ baseURL: TOOLS_API_BASE_URL });

// Add request interceptor for user ID
toolsApi.interceptors.request.use(
    (config) => {
        const userId = localStorage.getItem('userId');
        if (userId) {
            config.headers['x-user-id'] = userId;
        }
        if (!(config.data instanceof FormData)) {
            config.headers['Content-Type'] = 'application/json';
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// Add response interceptor for error handling
toolsApi.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response && error.response.status === 401) {
            console.warn("Tools API: 401 Unauthorized. Clearing auth & redirecting.");
            localStorage.clear();
            if (!window.location.pathname.includes('/login')) {
                window.location.href = '/login?sessionExpired=true';
            }
        }
        return Promise.reject(error);
    }
);

// --- NEW TOOLS API FUNCTIONS ---

// Search and download PDFs
export const searchAndDownloadPDFs = (query) => toolsApi.post('/api/tools/search_and_download', { query });

// Convert PDF to audio
export const convertPDFToAudio = (pdfFile) => toolsApi.post('/api/tools/convert_pdf_to_audio', { pdf_file: pdfFile });

// Process markdown to presentations
export const processMarkdown = (markdownContent) => toolsApi.post('/api/tools/process_markdown', { markdown_content: markdownContent });

// Fetch academic journals
export const fetchJournals = (query) => toolsApi.post('/api/tools/fetch_journals', { query });

// Open and download academic papers
export const openJournals = (query) => toolsApi.post('/api/tools/open_journals', { query });

// Health check for tools
export const checkToolsHealth = () => toolsApi.get('/api/tools/health');

export default toolsApi; 