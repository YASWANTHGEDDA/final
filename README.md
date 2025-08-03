# AI DRIVEN STUDENT CHATBOT

![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![Node.js](https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=nodedotjs&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white)

FusedChatbotNew is a complete-stack conversational AI system that uses a React UI, Node.js server, and Python-based AI core service. It enables smooth interaction with various large language models (LLMs) like Gemini, Groq, and Ollama, providing adaptable and smart conversation possibilities. With Retrieval-Augmented Generation (RAG), documents (PDF, DOCX, TXT, PPTX) can be uploaded by users to get highly relevant, context-sensitive answers. It performs sophisticated document analysis through auto-generated FAQs, key topics extraction, and the generation of mindmaps based on Mermaid. A special dual-voice podcast generator converts documents into immersive audio content, enabling users to pose real-time questions while listening. Other features include voice-to-text recognition, auto-generated flashcards and quizzes, and the execution of code within the chat itself. Users can handle files, view chat history, remove sessions, and have a simple, responsive UI that supports light/dark mode. A system for autonomous agents provides multi-step planning of tasks, tool operation, and self-modification. Caching using Redis for efficient performance and speed and secure user authorization along with admin-grade API key management ensure strong access and privacy. In all, FusedChatbotNew provides a rich, scalable platform for intelligent dialogue, document manipulation, and AI-assisted learning.

---
## FusedChatbot Overview : https://drive.google.com/file/d/1FP3Ahd1fW6KBfKrCaukBWjueHa4RA43t/view?usp=sharing 
## Code Overview : https://youtu.be/y3pUV6oN1wU?si=3GeETW5_nirLbIyo
## Installation Video : https://drive.google.com/file/d/1GD_JbBEaLgkipeuYwjFK3QYLk6scmMQY/view?usp=drive_link
---

## ✨ Features

*   *Multi-LLM Support:* Choose from Gemini, Groq LLaMA 3, or Ollama-hosted models for chat interactions.
*   *Retrieval Augmented Generation (RAG):* Upload documents (PDF, DOCX, PPTX, TXT) to augment chat responses with relevant context, including multi-query RAG for improved recall.
*   *Document Analysis:*
    *   *FAQ Generation:* Automatically extracts FAQs based on document content, scaling with document size.
    *   *Topic Identification:* Identifies key topics with explanations, dynamically adjusted by document length.
    *   *Mindmap Generation:* Creates hierarchical mindmaps using Mermaid for visualizing document structure.
*   *Chain-of-Thought (CoT):* Displays the AI's reasoning process for transparency in responses.
*   *User Management:* Supports user signup, signin, and session management.
*   *File Management:* Upload, list, rename, and delete user-specific documents.
*   *Chat History:* Save and retrieve chat sessions with RAG references and CoT.
*   *Voice-to-Text Recognition:* Convert spoken input into text for hands-free interaction.
*   *Chat Deletion:* Delete chat sessions for privacy and clutter management.
*   *Enhanced UI:* Modern, intuitive interface for a seamless user experience.
*   *Admin Pannel:* Users seeking access to Admin API keys can submit a request directly through the interface. Admins are automatically notified via email, and upon approval or rejection, users receive real-                        time status updates through email notifications.
*   *Autonomus Agent:* Automatically plan, execute, and adapt tasks using goal-driven logic powered by open-source models like LLaMA-3 and Zephyr  and it was equipped with a dynamic toolbox like smart_search, web_search to find answers
*   *Prompt Enhancer:* The system automatically rewrites user prompts to make them clearer and more focused, helps to  understand better and give more accurate answers.
*   *Quiz Generator:* Upload a document, and the system automatically builds a quiz from the content.
*   *Code Compiler:* Write and run code (Python, JS, etc.) directly in the chat with instant results.It also helps us to find errors and clearly explain with suggestions to improve or fix the code.
*   *Flashcard Generation:* Converts documents into ready-to-use flashcards with terms,definitions and concepts.
*   **Podcast Generator:** Converts any document or topic into an engaging AI-generated podcast featuring two distinct voices in a conversational format.Users can interact with the podcast in real time by pausing and asking follow-up questions, creating a dynamic learning experience.
*   *Chat Enhancement:* Uses Redis caching to deliver faster responses by storing commonly used answers, chat context, and document previews.

---

## 🏗 Architecture

This project uses a scalable *microservice-oriented architecture* to separate concerns and improve maintainability.

[React Frontend] ↔ [Node.js Backend (Orchestrator)] ↔ [Python AI Service (AI Core)]

*   *React Frontend:* A modern, dynamic user interface.
*   *Node.js Backend:* Acts as an orchestrator and API gateway. It handles user authentication, session management, and file operations. It does *not* contain heavy AI logic.
*   *Python AI Service:* A dedicated service for all specialized AI tasks, including RAG, vector database management (FAISS), and all communication with LLMs (Gemini, Groq, Ollama).

---

## 🛠 Tech Stack

*   *Frontend:* React, Axios
*   *Backend (Orchestrator):* Node.js, Express.js
*   *AI Service:* Python, Flask
*   *Database:* MongoDB with Mongoose
*   *AI & ML:*
    *   *LLMs:* Google Gemini, Groq, Ollama
    *   *Vector Database:* FAISS (Facebook AI Similarity Search)
    *   *Embeddings:* Sentence-Transformers
*   *Authentication:* JWT (JSON Web Tokens), bcrypt.js

---

## ✅ Prerequisites

*   *FFmpeg:* [Link](https://www.gyan.dev/ffmpeg/builds/)
        1.after download sucessful you need to add the bin directory to your system's envi path
*   *Node.js:* v16 or higher with npm.
*   *Python:* v3.9 or higher with pip.
*   *Git:* For cloning the repository.
*   *MongoDB:* A running instance (local MongoDB Community Server or a free MongoDB Atlas cluster).
*   *(Optional) Ollama:* Installed and running for local LLM support.

# Install Node.js (22.x) & npm
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo bash
sudo apt install -y nodejs

# Install Python 3.11 & pip
sudo apt update
sudo apt install -y python3.11 python3.11-venv python3.11-dev python3-pip

# Install MongoDB
curl -fsSL https://pgp.mongodb.com/server-6.0.asc | gpg -o /usr/share/keyrings/mongodb-server-6.0.gpg --dearmor
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-6.0.gpg ] https://repo.mongodb.org/apt/ubuntu $(lsb_release -cs)/mongodb-org/6.0 multiverse" > /etc/apt/sources.list.d/mongodb-org-6.0.list
sudo apt update
sudo apt install -y mongodb-org
systemctl start mongod
systemctl enable mongod

# Install ffmpeg
sudo apt update
sudo apt install ffmpeg

# Docker
sudo apt install -y docker.io
sudo systemctl enable --now docker

---

## 🚀 Getting Started

## ⚙ Setup and Installation

Follow these steps to set up and run the FusedChatbotNew project locally.

### Step 1: Clone the Repository

Clone the project from GitHub and navigate to the project directory:

```bash
git clone <your-repository-url>
cd FusedChatbotNew
```

---

## Step 2: Configure Environment Variables

### Backend (Node.js)

*   *Navigate to the server directory and create a .env file by copying the example file.
*   *Navigate to the server/ai_core_service directory and create a .env file by copying the example file.

```bash
cd server
```
```
# For Linux/macOS
cp .env.example .env

# For Windows
copy .env.example .env
```



---

## Step 3: Install Dependencies

### Backend (Node.js)

In the server directory, install the required Node.js dependencies:

```bash
cd server
npm install
```


---

#### AI Core Service Dependencies (Python)
```bash
cd ai_core_service
python -m venv venv

# Activate:
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Windows CMD
.\venv\Scripts\Activate.bat

# Linux/macOS
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

#### Frontend Dependencies (React)
```bash
cd ../../client
npm install
```
---
## Running the Application
###Run the three services in separate terminal windows
## Running the Neo4j services
```bash
docker run --name neo4j-db -p 7474:7474 -p 7687:7687 -d -e NEO4J_AUTH=neo4j/test neo4j:latest
```
## Running Redis services
```bash
docker run --name redis-server -p 6379:6379 -d redis:latest
```

### Terminal 1: Start the AI Core Service (Python)
```bash
cd server

# Activate virtual environment
cd ai_core_service

.\venv\Scripts\Activate.ps1  # Windows
# or
source ai_core_service/venv/bin/activate     # macOS/Linux

cd..  #run the command in the server
python -m ai_core_service.app
```

### Terminal 2: Start the Backend Server (Node.js)
```bash
cd server
node server.js
```

### Terminal 3: Start the Frontend (React)
```bash
cd client
npm start
```

## Accessing the Application
Go to: [http://localhost:3000](http://localhost:3000)
