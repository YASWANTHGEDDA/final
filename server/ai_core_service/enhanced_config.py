# Enhanced Configuration for AI Core Service
import os
import sys

# --- Determine Base Directory (ai_core_service) ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
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
FAISS_INDEX_DIR = os.path.join(SERVER_DIR, 'faiss_indices')
DEFAULT_ASSETS_DIR = os.path.join(SERVER_DIR, 'default_assets', 'engineering')
DEFAULT_INDEX_USER_ID = '__DEFAULT__'

# --- Enhanced Text Splitting Configuration ---
CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', 512))
CHUNK_OVERLAP = int(os.getenv('CHUNK_OVERLAP', 100))
ENABLE_SEMANTIC_CHUNKING = os.getenv('ENABLE_SEMANTIC_CHUNKING', 'true').lower() == 'true'
SEMANTIC_CHUNK_THRESHOLD = float(os.getenv('SEMANTIC_CHUNK_THRESHOLD', 0.7))

# --- API Configuration ---
AI_CORE_SERVICE_PORT = int(os.getenv('AI_CORE_SERVICE_PORT', 9000))
RAG_SERVICE_PORT = AI_CORE_SERVICE_PORT

# Analysis Configuration
ANALYSIS_MAX_CONTEXT_LENGTH = int(os.getenv('ANALYSIS_MAX_CONTEXT_LENGTH', 8000))

# --- Enhanced LLM and RAG Defaults ---
DEFAULT_LLM_PROVIDER = os.getenv("DEFAULT_LLM_PROVIDER", "ollama")
DEFAULT_RAG_K = int(os.getenv("DEFAULT_RAG_K", 3))
REFERENCE_SNIPPET_LENGTH = int(os.getenv("REFERENCE_SNIPPET_LENGTH", 200))

# --- Multi-Query RAG Configuration ---
MULTI_QUERY_COUNT_CONFIG = int(os.getenv("MULTI_QUERY_COUNT_CONFIG", 3))
DEFAULT_RAG_K_PER_SUBQUERY_CONFIG = int(os.getenv("DEFAULT_RAG_K_PER_SUBQUERY_CONFIG", 2))

# --- Advanced Prompt Engineering ---
ENABLE_DYNAMIC_PROMPTING = os.getenv('ENABLE_DYNAMIC_PROMPTING', 'true').lower() == 'true'
ENABLE_FEW_SHOT_LEARNING = os.getenv('ENABLE_FEW_SHOT_LEARNING', 'true').lower() == 'true'
ENABLE_CHAIN_OF_THOUGHT = os.getenv('ENABLE_CHAIN_OF_THOUGHT', 'true').lower() == 'true'

# --- Monitoring & Logging ---
ENABLE_PERFORMANCE_MONITORING = os.getenv('ENABLE_PERFORMANCE_MONITORING', 'true').lower() == 'true'
ENABLE_DETAILED_LOGGING = os.getenv('ENABLE_DETAILED_LOGGING', 'false').lower() == 'true'
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# --- Print effective configuration ---
if os.getenv('DEBUG_CONFIG', 'false').lower() == 'true':
    print("--- Enhanced AI Core Service Configuration ---")
    print(f"Using Sentence Transformer model: {EMBEDDING_MODEL_NAME}")
    print(f"Response Caching: {ENABLE_RESPONSE_CACHING}")
    print(f"Embedding Cache: {ENABLE_EMBEDDING_CACHE}")
    print(f"Query Expansion: {ENABLE_QUERY_EXPANSION}")
    print(f"Hybrid Search: {ENABLE_HYBRID_SEARCH}")
    print(f"Reranking: {ENABLE_RERANKING}")
    print(f"Dynamic Context Selection: {DYNAMIC_CONTEXT_SELECTION}")
    print(f"Max Concurrent Requests: {MAX_CONCURRENT_REQUESTS}")
    print("-------------------------------------------------") 