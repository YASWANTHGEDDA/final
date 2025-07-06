// server/routes/tools.js
const express = require('express');
const router = express.Router();
const axios = require('axios');
const fs = require('fs').promises;
const path = require('path');

// Configuration
const PYTHON_SERVICE_URL = process.env.PYTHON_AI_CORE_SERVICE_URL || 'http://localhost:9000';

// Helper function to make requests to Python service
async function callPythonService(endpoint, data) {
    try {
        const response = await axios.post(`${PYTHON_SERVICE_URL}${endpoint}`, data, {
            timeout: 30000, // 30 second timeout
            headers: {
                'Content-Type': 'application/json'
            }
        });
        return response.data;
    } catch (error) {
        console.error(`Error calling Python service ${endpoint}:`, error.message);
        throw new Error(error.response?.data?.error || error.message || 'Service unavailable');
    }
}

// 1. Search and Download PDFs
router.post('/search_and_download', async (req, res) => {
    try {
        const { query } = req.body;
        
        if (!query) {
            return res.status(400).json({ 
                error: 'Missing query parameter',
                status: 'error' 
            });
        }

        console.log(`[TOOLS] Search and download request: ${query}`);
        
        const result = await callPythonService('/search_and_download', { query });
        
        console.log(`[TOOLS] Search and download completed: ${result.files?.length || 0} files`);
        
        res.json({
            message: result.message || 'Search and download completed',
            files: result.files || [],
            status: 'success'
        });
        
    } catch (error) {
        console.error('[TOOLS] Search and download error:', error.message);
        res.status(500).json({ 
            error: error.message,
            status: 'error' 
        });
    }
});

// 2. Convert PDF to Audio
router.post('/convert_pdf_to_audio', async (req, res) => {
    try {
        const { pdf_file } = req.body;
        
        if (!pdf_file) {
            return res.status(400).json({ 
                error: 'Missing pdf_file parameter',
                status: 'error' 
            });
        }

        console.log(`[TOOLS] PDF to audio conversion request: ${pdf_file}`);
        
        const result = await callPythonService('/convert_pdf_to_audio', { pdf_file });
        
        console.log(`[TOOLS] PDF to audio conversion completed: ${result.audio_files?.length || 0} files`);
        
        res.json({
            message: result.message || 'Audio conversion completed',
            audio_files: result.audio_files || [],
            status: 'success'
        });
        
    } catch (error) {
        console.error('[TOOLS] PDF to audio conversion error:', error.message);
        res.status(500).json({ 
            error: error.message,
            status: 'error' 
        });
    }
});

// 3. Process Markdown to Presentations
router.post('/process_markdown', async (req, res) => {
    try {
        const { markdown_content } = req.body;
        
        if (!markdown_content) {
            return res.status(400).json({ 
                error: 'Missing markdown_content parameter',
                status: 'error' 
            });
        }

        console.log(`[TOOLS] Markdown processing request: ${markdown_content.length} characters`);
        
        const result = await callPythonService('/process_markdown', { markdown_content });
        
        console.log(`[TOOLS] Markdown processing completed: ${result.files?.length || 0} files`);
        
        res.json({
            message: result.message || 'Markdown processed and files generated',
            files: result.files || [],
            status: 'success'
        });
        
    } catch (error) {
        console.error('[TOOLS] Markdown processing error:', error.message);
        res.status(500).json({ 
            error: error.message,
            status: 'error' 
        });
    }
});

// 4. Fetch Academic Journals
router.post('/fetch_journals', async (req, res) => {
    try {
        const { query } = req.body;
        
        if (!query) {
            return res.status(400).json({ 
                error: 'Missing query parameter',
                status: 'error' 
            });
        }

        console.log(`[TOOLS] Fetch journals request: ${query}`);
        
        const result = await callPythonService('/fetch_journals', { query });
        
        console.log(`[TOOLS] Fetch journals completed`);
        
        res.json({
            message: result.message || 'Journals fetched',
            data: result.data || '[]',
            status: 'success'
        });
        
    } catch (error) {
        console.error('[TOOLS] Fetch journals error:', error.message);
        res.status(500).json({ 
            error: error.message,
            status: 'error' 
        });
    }
});

// 5. Open and Download Academic Papers
router.post('/open_journals', async (req, res) => {
    try {
        const { query } = req.body;
        
        if (!query) {
            return res.status(400).json({ 
                error: 'Missing query parameter',
                status: 'error' 
            });
        }

        console.log(`[TOOLS] Open journals request: ${query}`);
        
        const result = await callPythonService('/open_journals', { query });
        
        console.log(`[TOOLS] Open journals completed`);
        
        res.json({
            message: result.message || 'Journals opened',
            data: result.data || '[]',
            status: 'success'
        });
        
    } catch (error) {
        console.error('[TOOLS] Open journals error:', error.message);
        res.status(500).json({ 
            error: error.message,
            status: 'error' 
        });
    }
});

// 6. Health check for tools
router.get('/health', async (req, res) => {
    try {
        // Check if Python service is available
        const pythonHealth = await axios.get(`${PYTHON_SERVICE_URL}/health`, { timeout: 5000 });
        
        res.json({
            status: 'ok',
            tools_available: true,
            python_service: pythonHealth.data,
            message: 'Tools service is healthy'
        });
        
    } catch (error) {
        res.status(503).json({
            status: 'error',
            tools_available: false,
            error: 'Python AI Core service is not available',
            message: error.message
        });
    }
});

module.exports = router; 