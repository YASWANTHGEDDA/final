# FusedChatbot/server/ai_core_service/config.py
import os
import sys

# --- Determine Base Directory (ai_core_service) ---
# CURRENT_DIR is the directory where this config.py file is located (ai_core_service)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# SERVER_DIR is the parent of CURRENT_DIR (which should be 'server')
# This is useful if FAISS_INDEX_DIR or DEFAULT_ASSETS_DIR are outside ai_core_service
# and within the main 'server' directory.
SERVER_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '..'))

# --- Enhanced Embedding Model Configuration ---
EMBEDDING_TYPE = 'sentence-transformer'
EMBEDDING_MODEL_NAME_ST = os.getenv('SENTENCE_TRANSFORMER_MODEL', 'mixedbread-ai/mxbai-embed-large-v1')
EMBEDDING_MODEL_NAME = EMBEDDING_MODEL_NAME_ST

# --- Performance & Caching Configuration ---
ENABLE_RESPONSE_CACHING = os.getenv('ENABLE_RESPONSE_CACHING', 'true').lower() == 'true'
CACHE_TTL_SECONDS = int(os.getenv('CACHE_TTL_SECONDS', 3600))  # 1 hour default
ENABLE_EMBEDDING_CACHE = os.getenv('ENABLE_EMBEDDING_CACHE', 'true').lower() == 'true'
EMBEDDING_CACHE_SIZE = int(os.getenv('EMBEDDING_CACHE_SIZE', 10000))  # LRU cache size

# --- Advanced RAG Configuration ---
ENABLE_QUERY_EXPANSION = os.getenv('ENABLE_QUERY_EXPANSION', 'true').lower() == 'true'
QUERY_EXPANSION_MODEL = os.getenv('QUERY_EXPANSION_MODEL', 'gpt-3.5-turbo')
ENABLE_HYBRID_SEARCH = os.getenv('ENABLE_HYBRID_SEARCH', 'true').lower() == 'true'
ENABLE_RERANKING = os.getenv('ENABLE_RERANKING', 'true').lower() == 'true'
RERANKING_MODEL = os.getenv('RERANKING_MODEL', 'ms-marco-MiniLM-L-6-v2')

# --- Context Management ---
MAX_CONTEXT_LENGTH = int(os.getenv('MAX_CONTEXT_LENGTH', 8000))
DYNAMIC_CONTEXT_SELECTION = os.getenv('DYNAMIC_CONTEXT_SELECTION', 'true').lower() == 'true'
CONTEXT_OVERLAP_RATIO = float(os.getenv('CONTEXT_OVERLAP_RATIO', 0.1))

# --- Rate Limiting & Performance ---
MAX_CONCURRENT_REQUESTS = int(os.getenv('MAX_CONCURRENT_REQUESTS', 10))
REQUEST_TIMEOUT_SECONDS = int(os.getenv('REQUEST_TIMEOUT_SECONDS', 120))
ENABLE_REQUEST_QUEUING = os.getenv('ENABLE_REQUEST_QUEUING', 'true').lower() == 'true'

# --- FAISS Configuration ---
# Store FAISS indices within the main 'server' directory, not inside ai_core_service
FAISS_INDEX_DIR = os.path.join(SERVER_DIR, 'faiss_indices')
# Store default assets within the main 'server' directory
DEFAULT_ASSETS_DIR = os.path.join(SERVER_DIR, 'default_assets', 'engineering') # Or your chosen default path
DEFAULT_INDEX_USER_ID = '__DEFAULT__'

# --- Enhanced Text Splitting Configuration ---
CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', 512))
CHUNK_OVERLAP = int(os.getenv('CHUNK_OVERLAP', 100))
ENABLE_SEMANTIC_CHUNKING = os.getenv('ENABLE_SEMANTIC_CHUNKING', 'true').lower() == 'true'
SEMANTIC_CHUNK_THRESHOLD = float(os.getenv('SEMANTIC_CHUNK_THRESHOLD', 0.7))

# --- API Configuration ---
AI_CORE_SERVICE_PORT = int(os.getenv('AI_CORE_SERVICE_PORT', 9000))
# Kept RAG_SERVICE_PORT for backward compatibility if anything still uses it, but prefer AI_CORE_SERVICE_PORT
RAG_SERVICE_PORT = AI_CORE_SERVICE_PORT # Alias for consistency

# Analysis Configuration
ANALYSIS_MAX_CONTEXT_LENGTH = int(os.getenv('ANALYSIS_MAX_CONTEXT_LENGTH', 8000))

# --- Enhanced LLM and RAG Defaults ---
DEFAULT_LLM_PROVIDER = os.getenv("DEFAULT_LLM_PROVIDER", "ollama")  # 'ollama', 'gemini', or 'groq_llama3'
DEFAULT_RAG_K = int(os.getenv("DEFAULT_RAG_K", 3))                  # Default number of RAG documents for single query RAG
REFERENCE_SNIPPET_LENGTH = int(os.getenv("REFERENCE_SNIPPET_LENGTH", 200)) # For client display

# --- Multi-Query RAG Configuration (NEW - REQUIRED BY app.py) ---
MULTI_QUERY_COUNT_CONFIG = int(os.getenv("MULTI_QUERY_COUNT_CONFIG", 3)) # Default number of sub-queries to generate
DEFAULT_RAG_K_PER_SUBQUERY_CONFIG = int(os.getenv("DEFAULT_RAG_K_PER_SUBQUERY_CONFIG", 2)) # Default K for each sub-query search

# --- Advanced Prompt Engineering ---
ENABLE_DYNAMIC_PROMPTING = os.getenv('ENABLE_DYNAMIC_PROMPTING', 'true').lower() == 'true'
ENABLE_FEW_SHOT_LEARNING = os.getenv('ENABLE_FEW_SHOT_LEARNING', 'true').lower() == 'true'
ENABLE_CHAIN_OF_THOUGHT = os.getenv('ENABLE_CHAIN_OF_THOUGHT', 'true').lower() == 'true'

# --- Monitoring & Logging ---
ENABLE_PERFORMANCE_MONITORING = os.getenv('ENABLE_PERFORMANCE_MONITORING', 'true').lower() == 'true'
ENABLE_DETAILED_LOGGING = os.getenv('ENABLE_DETAILED_LOGGING', 'false').lower() == 'true'
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# --- Optional: Default Model Names for LLM Providers (Can also be set in .env for llm_handler.py) ---
# These are fallback values if not set in the .env file that llm_handler.py reads
# OLLAMA_DEFAULT_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
# GEMINI_DEFAULT_MODEL = os.getenv("GEMINI_MODEL_NAME", "gemini-1.5-flash")
# GROQ_LLAMA3_DEFAULT_MODEL = os.getenv("GROQ_LLAMA3_MODEL", "llama3-8b-8192")


# --- Print effective configuration (optional, for debugging during startup) ---
# To enable these prints, you might set an environment variable like DEBUG_CONFIG=true
if os.getenv('DEBUG_CONFIG', 'false').lower() == 'true':
    print("--- Enhanced AI Core Service Configuration (config.py) ---")
    print(f"CURRENT_DIR (ai_core_service): {CURRENT_DIR}")
    print(f"SERVER_DIR (parent of ai_core_service): {SERVER_DIR}")
    print(f"Using Sentence Transformer model: {EMBEDDING_MODEL_NAME}")
    print(f"FAISS Index Directory: {FAISS_INDEX_DIR}")
    print(f"Default Assets Directory: {DEFAULT_ASSETS_DIR}")
    print(f"AI Core Service Port: {AI_CORE_SERVICE_PORT}")
    print(f"Default Index User ID: {DEFAULT_INDEX_USER_ID}")
    print(f"Chunk Size: {CHUNK_SIZE}, Chunk Overlap: {CHUNK_OVERLAP}")
    print(f"Default LLM Provider: {DEFAULT_LLM_PROVIDER}")
    print(f"Default RAG K (single query): {DEFAULT_RAG_K}")
    print(f"Reference Snippet Length: {REFERENCE_SNIPPET_LENGTH}")
    print(f"Multi-Query Count Config: {MULTI_QUERY_COUNT_CONFIG}")
    print(f"Default RAG K per Sub-Query Config: {DEFAULT_RAG_K_PER_SUBQUERY_CONFIG}")
    print(f"Response Caching: {ENABLE_RESPONSE_CACHING}")
    print(f"Embedding Cache: {ENABLE_EMBEDDING_CACHE}")
    print(f"Query Expansion: {ENABLE_QUERY_EXPANSION}")
    print(f"Hybrid Search: {ENABLE_HYBRID_SEARCH}")
    print(f"Reranking: {ENABLE_RERANKING}")
    print(f"Dynamic Context Selection: {DYNAMIC_CONTEXT_SELECTION}")
    print(f"Max Concurrent Requests: {MAX_CONCURRENT_REQUESTS}")
    print("-------------------------------------------------")