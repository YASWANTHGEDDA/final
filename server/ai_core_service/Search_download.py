#pip install duckduckgo_search google-generativeai arxiv
from dotenv import load_dotenv
import duckduckgo_search
import requests
import os
import google.generativeai as genai
import arxiv
import re

# Load environment variables from .env file
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini API setup (now loads from .env)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

# Search query
query = "Machine learning textbooks and lecture notes filetype:pdf"

# DuckDuckGo search
ddg = duckduckgo_search.DDGS()
results = ddg.text(query, max_results=100)

# Save links to links.txt
with open("pdf_links.txt", "w") as f:
    for result in results:
        f.write(result["href"] + "\n")

# Function to check if URL is a PDF
def is_pdf(url):
    return url.lower().endswith('.pdf')

def is_arxiv_url(url):
    return "arxiv.org" in url

# Ensure 'pdfs' directory exists
PDF_DIR = os.path.join(os.path.dirname(__file__), 'pdfs')
os.makedirs(PDF_DIR, exist_ok=True)

def download_arxiv_pdf(arxiv_id, filename):
    try:
        search = arxiv.Search(id_list=[arxiv_id])
        result = next(search.results())
        response = requests.get(result.pdf_url, stream=True, timeout=10)
        response.raise_for_status()

        file_path = os.path.join(PDF_DIR, filename)
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded: {file_path}")

    except Exception as e:
        print(f"Error downloading arXiv PDF: {e}")

# Download PDFs
def download_pdf(url, index):
    try:
        response = requests.get(url, stream=True, timeout=10)
        if response.status_code == 200 and 'application/pdf' in response.headers.get('Content-Type', ''):
            filename = f"pdf_{index}.pdf"
            file_path = os.path.join(PDF_DIR, filename)
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded: {file_path}")
    except Exception:
        pass

# Create pdf_links.txt if it doesn't exist, or read from it if it does
if not os.path.exists("pdf_links.txt"):
    open("pdf_links.txt", "w").close()  # Create an empty file

# Read links from pdf_links.txt
with open("pdf_links.txt", "r") as f:
    links = f.readlines()

# Gemini API to filter relevant links
relevant_links = []
for link in links:
    link = link.strip()
    prompt = f"Is this link relevant to AI and LLM driven agents? URL: {link}"
    try:
        response = model.generate_content(prompt, generation_config=genai.GenerationConfig(max_output_tokens=50))
        if "yes" in response.text.lower():
            relevant_links.append(link)
    except Exception as e:
        print(f"Error processing link {link} with Gemini: {e}")

# Download PDFs from relevant links
for i, link in enumerate(relevant_links):
    link = link.strip()
    if is_pdf(link):
        if is_arxiv_url(link):
            # Extract arXiv ID
            match = re.search(r'arxiv\.org/abs/(\d+\.\d+)', link)
            if match:
                arxiv_id = match.group(1)
                filename = f"arxiv_{arxiv_id}.pdf"
                download_arxiv_pdf(arxiv_id, filename)
            else:
                download_pdf(link, i)
        else:
            download_pdf(link, i)

# =========================
# Model Context Protocol
# =========================

class ResourceContext:
    def __init__(self, query, resource_types=None):
        self.query = query
        self.resource_types = resource_types or ['pdf', 'webpage', 'video']
        self.results = []  # List of dicts: {type, url, title, local_path, metadata}

class ResourceModule:
    def process(self, context: ResourceContext):
        raise NotImplementedError

# PDF Module
class PDFModule(ResourceModule):
    def process(self, context: ResourceContext):
        ddg = duckduckgo_search.DDGS()
        pdf_query = f"{context.query} filetype:pdf"
        results = ddg.text(pdf_query, max_results=20)
        for i, result in enumerate(results):
            url = result["href"]
            title = result.get("title", "PDF Document")
            if url.lower().endswith('.pdf'):
                try:
                    response = requests.get(url, stream=True, timeout=10)
                    if response.status_code == 200 and 'application/pdf' in response.headers.get('Content-Type', ''):
                        filename = f"pdf_{i}.pdf"
                        file_path = os.path.join(PDF_DIR, filename)
                        with open(file_path, 'wb') as f:
                            f.write(response.content)
                        context.results.append({
                            'type': 'pdf',
                            'url': url,
                            'title': title,
                            'local_path': file_path,
                            'metadata': {}
                        })
                except Exception as e:
                    print(f"Error downloading PDF: {e}")

# Webpage Module (implemented)
class WebpageModule(ResourceModule):
    def process(self, context: ResourceContext):
        ddg = duckduckgo_search.DDGS()
        web_query = f"{context.query} site:.com OR site:.org OR site:.edu"
        results = ddg.text(web_query, max_results=10)
        for i, result in enumerate(results):
            url = result["href"]
            title = result.get("title", "Webpage")
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200 and 'text/html' in response.headers.get('Content-Type', ''):
                    filename = f"webpage_{i}.html"
                    file_path = os.path.join(os.path.dirname(__file__), 'webpages', filename)
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(response.text)
                    context.results.append({
                        'type': 'webpage',
                        'url': url,
                        'title': title,
                        'local_path': file_path,
                        'metadata': {'content_type': 'text/html'}
                    })
            except Exception as e:
                print(f"Error downloading webpage: {e}")

# YouTube Module (implemented: collects video URLs and titles)
class YouTubeModule(ResourceModule):
    def process(self, context: ResourceContext):
        ddg = duckduckgo_search.DDGS()
        yt_query = f"{context.query} site:youtube.com"
        results = ddg.text(yt_query, max_results=10)
        for result in results:
            url = result["href"]
            title = result.get("title", "YouTube Video")
            if 'youtube.com/watch' in url:
                context.results.append({
                    'type': 'youtube',
                    'url': url,
                    'title': title,
                    'local_path': None,  # Not downloaded yet
                    'metadata': {'source': 'YouTube'}
                })

# Orchestrator

def gather_resources(query, resource_types=None):
    context = ResourceContext(query, resource_types)
    modules = [PDFModule(), WebpageModule(), YouTubeModule()]
    for module in modules:
        module.process(context)
    return context.results

# Example usage (for testing):
if __name__ == "__main__":
    topic = "Machine learning textbooks and lecture notes"
    results = gather_resources(topic)
    print("Gathered resources:")
    for res in results:
        print(res)
