# FusedChatbot/server/ai_core_service/app.py
import os
import sys
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS

# --- Standard Local Module Imports ---
# This block correctly handles path adjustments for different execution contexts.
try:
    from . import config, file_parser, faiss_handler, llm_handler
except ImportError:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    import config, file_parser, faiss_handler, llm_handler

# --- Optional Tool/Module Imports (Corrected) ---
# Modules are now imported only ONCE at startup. This is efficient and correct.
# The try/except blocks make the app robust if a tool's .py file is missing.
try:
    from . import search_and_download
except ImportError:
    search_and_download = None
try:
    from . import pdf_to_audio_converter as pdf2audio # Using an alias for brevity
except ImportError:
    pdf2audio = None
try:
    from . import markdown_processor as md_processor
except ImportError:
    md_processor = None
try:

    from . import journal_fetch
except ImportError:
    journal_fetch = None
try:
    from . import journal_open
except ImportError:
    journal_open = None

# --- Application Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - [%(name)s:%(lineno)d] - %(message)s')
logger = logging.getLogger(__name__)
app = Flask(__name__)
CORS(app)

def create_error_response(message, status_code=500):
    logger.error(f"API Error Response ({status_code}): {message}")
    return jsonify({"error": message, "status": "error"}), status_code

# --- API Routes ---

@app.route('/health', methods=['GET'])
def health_check():
    logger.info("\n--- Received request at /health ---")
    status_details = {
        "status": "error", "embedding_model_type": config.EMBEDDING_TYPE,
        "embedding_model_name": config.EMBEDDING_MODEL_NAME, "embedding_dimension": None,
        "sentence_transformer_load": "Unknown", "default_index_loaded": False,
        "gemini_sdk_installed": bool(llm_handler.genai), "ollama_available": bool(llm_handler.ollama_available),
        "groq_sdk_installed": bool(llm_handler.Groq), "message": ""
    }
    http_status_code = 503
    try:
        model = faiss_handler.embedding_model
        if model is None:
            raise RuntimeError("Embedding model could not be initialized.")
        status_details["sentence_transformer_load"] = "OK"
        status_details["embedding_dimension"] = faiss_handler.get_embedding_dimension(model)
        status_details["default_index_loaded"] = config.DEFAULT_INDEX_USER_ID in faiss_handler.loaded_indices
        if not status_details["default_index_loaded"]:
            status_details["message"] = "Default index is not loaded. It will be loaded on first use."
        if status_details["sentence_transformer_load"] == "OK":
            status_details["status"] = "ok"
            status_details["message"] = "AI Core service is running. Embeddings OK."
            http_status_code = 200
    except Exception as e:
        logger.error(f"--- Health Check Critical Error ---", exc_info=True)
        status_details["message"] = f"Health check failed critically: {str(e)}"
    return jsonify(status_details), http_status_code

@app.route('/search_and_download', methods=['POST'])
def handle_search_and_download():
    logger.info("\n--- Received request at /search_and_download ---")
    if search_and_download is None:
        return create_error_response("The 'search_and_download' tool is not available on the server.", 501)

    data = request.get_json()
    if not data or not data.get('query'):
        return create_error_response("Missing 'query' in JSON body", 400)

    try:
        results = search_and_download.perform_search_and_download(data['query'])
        return jsonify({"message": "Search and download completed", "files": results, "status": "success"}), 200
    except Exception as e:
        logger.error(f"Error in /search_and_download: {e}", exc_info=True)
        return create_error_response(f"Failed to perform search and download: {str(e)}", 500)

@app.route('/convert_pdf_to_audio', methods=['POST'])
def handle_convert_pdf_to_audio():
    logger.info("\n--- Received request at /convert_pdf_to_audio ---")
    if pdf2audio is None:
        return create_error_response("The 'pdf_to_audio_converter' tool is not available on the server.", 501)

    data = request.get_json()
    pdf_file = data.get('pdf_file') if data else None
    if not pdf_file:
        return create_error_response("Missing 'pdf_file' parameter", 400)
    if not os.path.exists(pdf_file):
        return create_error_response(f"PDF file not found: {pdf_file}", 404)

    try:
        audio_files = pdf2audio.convert_pdf_to_audiobook(pdf_file)
        return jsonify({"message": "Audio conversion completed", "audio_files": audio_files or [], "status": "success"}), 200
    except Exception as e:
        logger.error(f"Error in /convert_pdf_to_audio: {e}", exc_info=True)
        return create_error_response(f"Failed to convert PDF to audio: {str(e)}", 500)

@app.route('/process_markdown', methods=['POST'])
def handle_process_markdown():
    logger.info("\n--- Received request at /process_markdown ---")
    if md_processor is None:
        return create_error_response("The 'markdown_processor' tool is not available on the server.", 501)

    data = request.get_json()
    markdown_content = data.get('markdown_content') if data else None
    if not markdown_content:
        return create_error_response("Missing 'markdown_content' parameter", 400)

    try:
        # Assuming md_processor functions handle file creation and return paths
        slides_data = md_processor.refined_parse_markdown(markdown_content)
        # You would add your logic here to call create_ppt, create_doc, etc.
        # and collect the returned file paths.
        generated_files = [] # Populate this list with file paths from md_processor
        return jsonify({"message": "Markdown processed successfully", "files": generated_files, "status": "success"}), 200
    except Exception as e:
        logger.error(f"Error in /process_markdown: {e}", exc_info=True)
        return create_error_response(f"Failed to process markdown: {str(e)}", 500)

@app.route('/fetch_journals', methods=['POST'])
def handle_fetch_journals():
    logger.info("\n--- Received request at /fetch_journals ---")
    if journal_fetch is None:
        return create_error_response("The 'journal_fetch' tool is not available on the server.", 501)

    data = request.get_json()
    query = data.get('query') if data else None
    if not query:
        return create_error_response("Missing 'query' parameter", 400)

    try:
        df = journal_fetch.search_openalex(query)
        result_json = df.to_json(orient='records') if hasattr(df, 'to_json') else str(df)
        return jsonify({"message": "Journals fetched", "data": result_json, "status": "success"}), 200
    except Exception as e:
        logger.error(f"Error in /fetch_journals: {e}", exc_info=True)
        return create_error_response(f"Failed to fetch journals: {str(e)}", 500)

@app.route('/open_journals', methods=['POST'])
def handle_open_journals():
    logger.info("\n--- Received request at /open_journals ---")
    if journal_open is None:
        return create_error_response("The 'journal_open' tool is not available on the server.", 501)

    data = request.get_json()
    query = data.get('query') if data else None
    if not query:
        return create_error_response("Missing 'query' parameter", 400)

    try:
        df = journal_open.fetch_all_core_results(query)
        result_json = df.to_json(orient='records') if hasattr(df, 'to_json') else str(df)
        return jsonify({"message": "Journals opened", "data": result_json, "status": "success"}), 200
    except Exception as e:
        logger.error(f"Error in /open_journals: {e}", exc_info=True)
        return create_error_response(f"Failed to open journals: {str(e)}", 500)

@app.route('/add_document', methods=['POST'])
def add_document():
    logger.info("\n--- Received request at /add_document ---")
    if not request.is_json: return create_error_response("Request must be JSON", 400)
    data = request.get_json()
    if data is None: return create_error_response("Invalid or empty JSON body", 400)
    user_id = data.get('user_id'); file_path = data.get('file_path'); original_name = data.get('original_name')
    if not all([user_id, file_path, original_name]): return create_error_response("Missing required fields", 400)
    if not os.path.exists(file_path): return create_error_response(f"File not found: {file_path}", 404)
    try:
        text = file_parser.parse_file(file_path)
        if not text or not text.strip(): return jsonify({"message": f"No text in '{original_name}'.", "status": "skipped"}), 200
        docs = file_parser.chunk_text(text, original_name, user_id)
        faiss_handler.add_documents_to_index(user_id, docs)
        return jsonify({"message": f"'{original_name}' added.", "chunks_added": len(docs), "status": "added"}), 200
    except Exception as e: return create_error_response(f"Failed to process '{original_name}': {e}", 500)

@app.route('/query_rag_documents', methods=['POST'])
def query_rag_documents_route():
    logger.info("\n--- Received request at /query_rag_documents ---")
    if not request.is_json: return create_error_response("Request must be JSON", 400)
    data = request.get_json()
    if data is None: return create_error_response("Invalid or empty JSON body", 400)
    user_id = data.get('user_id'); query_text = data.get('query'); k = data.get('k', 5)
    if not user_id or not query_text: return create_error_response("Missing user_id or query", 400)
    try:
        results = faiss_handler.query_index(user_id, query_text, k=k)
        formatted = [{"documentName": d.metadata.get("documentName"), "score": float(s), "content": d.page_content} for d, s in results]
        return jsonify({"relevantDocs": formatted, "status": "success"}), 200
    except Exception as e: return create_error_response(f"Failed to query index: {e}", 500)

@app.route('/analyze_document', methods=['POST'])
def analyze_document_route():
    logger.info("\n--- Received request at /analyze_document ---")
    if not request.is_json: return create_error_response("Request must be JSON", 400)
    data = request.get_json()
    if data is None: return create_error_response("Invalid or empty JSON body", 400)

    user_id = data.get('user_id')
    document_name = data.get('document_name')
    analysis_type = data.get('analysis_type')
    file_path_for_analysis = data.get('file_path_for_analysis')
    llm_provider = data.get('llm_provider')
    llm_model_name = data.get('llm_model_name')
    api_keys = data.get('api_keys', {})
    ollama_host = data.get('ollama_host') or (api_keys.get('ollamaHost') if api_keys else None)
    if ollama_host:
        api_keys['ollama_host'] = ollama_host.strip()

    if not all([user_id, document_name, analysis_type, file_path_for_analysis]):
         return create_error_response("Missing required fields", 400)
    if not os.path.exists(file_path_for_analysis):
        return create_error_response(f"Document not found at path: {file_path_for_analysis}", 404)

    try:
        document_text = file_parser.parse_file(file_path_for_analysis)
        if not document_text or not document_text.strip():
            return create_error_response("Could not parse text from the document.", 400)

        analysis_result, thinking_content = llm_handler.perform_document_analysis(
            document_text=document_text, analysis_type=analysis_type,
            llm_provider=llm_provider, llm_model_name=llm_model_name,
            api_keys=api_keys, ollama_host=ollama_host
        )
        return jsonify({
            "analysis_result": analysis_result, "thinking_content": thinking_content,
            "document_name": document_name, "analysis_type": analysis_type, "status": "success"
        }), 200
    except Exception as e:
        return create_error_response(f"Failed to perform analysis: {str(e)}", 500)

@app.route('/generate_chat_response', methods=['POST'])
def generate_chat_response_route():
    logger.info("\n--- Received request at /generate_chat_response ---")
    if not request.is_json: return create_error_response("Request must be JSON", 400)
    data = request.get_json()
    if data is None: return create_error_response("Invalid or empty JSON body", 400)

    user_id = data.get('user_id')
    current_user_query = data.get('query')
    if not user_id or not current_user_query:
        return create_error_response("Missing user_id or query in request", 400)

    chat_history = data.get('chat_history', [])
    system_prompt = data.get('system_prompt')
    llm_provider = data.get('llm_provider', config.DEFAULT_LLM_PROVIDER)
    llm_model_name = data.get('llm_model_name', None)
    perform_rag = data.get('perform_rag', True)
    enable_multi_query = data.get('enable_multi_query', True)
    api_keys_data = data.get('api_keys', {})
    user_gemini_api_key = api_keys_data.get('gemini')
    user_grok_api_key = api_keys_data.get('grok')
    ollama_host = data.get('ollama_host', None)
    active_file = data.get('active_file')

    context_text_for_llm = "No relevant context was found."
    rag_references_for_client = []
    if perform_rag:
        try:
            queries_to_search = [current_user_query]
            if enable_multi_query:
                sub_queries = llm_handler.generate_sub_queries_via_llm(
                    original_query=current_user_query, llm_provider=llm_provider,
                    llm_model_name=llm_model_name, user_gemini_api_key=user_gemini_api_key,
                    user_grok_api_key=user_grok_api_key
                )
                if sub_queries:
                    queries_to_search.extend(sub_queries)
            unique_chunks = set()
            docs_for_context = []
            for q in set(queries_to_search):
                results = faiss_handler.query_index(user_id, q, k=config.DEFAULT_RAG_K_PER_SUBQUERY_CONFIG, active_file=active_file)
                for doc, score in results:
                    if doc.page_content not in unique_chunks:
                        unique_chunks.add(doc.page_content)
                        docs_for_context.append((doc, score))
            if docs_for_context:
                context_parts = [f"[{i+1}] Source: {d.metadata.get('documentName')}\n{d.page_content}" for i, (d, s) in enumerate(docs_for_context)]
                context_text_for_llm = "\n\n---\n\n".join(context_parts)
                rag_references_for_client = [{"documentName": d.metadata.get("documentName"), "score": float(s)} for d, s in docs_for_context]
        except Exception as e:
            logger.error(f"Error during RAG processing: {e}", exc_info=True)
            # Do not stop execution, proceed with no context.

    try:
        provider, model = llm_handler.select_llm_provider_and_model(current_user_query)
        final_answer, thinking_content = llm_handler.smart_generate_response(
            query=current_user_query, context_text=context_text_for_llm,
            chat_history=chat_history, system_prompt=system_prompt,
            llm_model_name=llm_model_name, user_gemini_api_key=user_gemini_api_key,
            user_grok_api_key=user_grok_api_key, ollama_host=ollama_host
        )
        return jsonify({
            "llm_response": final_answer, "references": rag_references_for_client,
            "thinking_content": thinking_content,
            "llm_debug": {"selected_provider": provider, "selected_model": model},
            "status": "success"
        }), 200
    except ConnectionError as e:
        return create_error_response(str(e), 502)
    except Exception as e:
        logger.error(f"Failed to generate chat response: {e}", exc_info=True)
        return create_error_response(f"Failed to generate chat response: {str(e)}", 500)


# --- Main Application Entry Point ---
if __name__ == '__main__':
    try:
        faiss_handler.ensure_faiss_dir()
        faiss_handler.get_embedding_model()
        faiss_handler.load_or_create_index(config.DEFAULT_INDEX_USER_ID)
    except Exception as e:
        logger.critical(f"CRITICAL STARTUP FAILURE: Could not initialize FAISS or embedding model. Error: {e}", exc_info=True)
        sys.exit(1)
    
    port = config.AI_CORE_SERVICE_PORT
    host = '0.0.0.0'
    logger.info(f"--- Starting AI Core Service (Flask App) on http://{host}:{port} ---")
    logger.info(f"Gemini SDK Installed: {bool(llm_handler.genai)}")
    logger.info(f"Groq SDK Installed: {bool(llm_handler.Groq)}") # <-- THIS LINE IS NOW CORRECT
    logger.info(f"Ollama Available: {llm_handler.ollama_available}")
    logger.info("---------------------------------------------")
    app.run(host=host, port=port, debug=os.getenv('FLASK_DEBUG', 'false').lower() == 'true')