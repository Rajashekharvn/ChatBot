# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

**StanChatBot** is a conversational AI chatbot powered by Google's Gemini API. The project consists of:

1. **Python Flask Backend** (`app.py`) - Main chatbot service with dual memory systems
2. **Web Frontend** (`templates/index.html`) - Responsive web interface with floating chat widget
3. **Rust Project** (`Rust_Project/`) - Incomplete Rust component (contains only skeleton code)

## Architecture & Memory Systems

The chatbot implements a **dual memory architecture**:

### SQLite Memory (`memory.db`)
- Stores structured conversation history per user
- Sequential chat interactions (user messages + bot replies)
- Used for maintaining conversation context (last 5 interactions)
- Functions: `save_memory()`, `get_memory()`, database connection management

### ChromaDB Vector Memory (`chroma_data/`)
- Semantic memory using sentence transformers (`all-MiniLM-L6-v2`)
- Enables similarity-based conversation recall
- Functions: `save_vector_memory()`, `recall_vector_memory()`
- Note: Vector memory functionality is implemented but not actively used in current chat flow

### Key Technical Components
- **AI Model**: Google Gemini-1.5-flash via `google-generativeai` library
- **Embeddings**: SentenceTransformers for semantic similarity
- **CORS**: Enabled for cross-origin requests
- **User Management**: Per-user conversation isolation using user_id

## Common Development Commands

### Python Flask Application

**Install Dependencies:**
```powershell path=null start=null
pip install -r requirements.txt
```

**Run Development Server:**
```powershell path=null start=null
python app.py
```
Server runs on `http://localhost:5000` by default.

**Environment Setup:**
Ensure `.env` file contains:
```bash path=null start=null
GEMINI_API_KEY="your_gemini_api_key_here"
```

### Rust Project

**Build Rust Project:**
```powershell path=null start=null
cd Rust_Project
cargo build
```

**Run Rust Project:**
```powershell path=null start=null
cd Rust_Project
cargo run
```
Note: Current Rust code contains only skeleton implementation with `todo!()` macro.

### Testing & Development

**Test Flask Endpoint:**
```powershell path=null start=null
curl -X POST http://localhost:5000/chat -H "Content-Type: application/json" -d '{\"user_id\":\"test\",\"message\":\"Hello\"}'
```

**Database Inspection:**
SQLite database can be inspected using any SQLite client:
```powershell path=null start=null
# Using sqlite3 command line (if available)
sqlite3 memory.db ".tables"
sqlite3 memory.db "SELECT * FROM memory LIMIT 10;"
```

## Development Workflow

1. **Backend Changes**: Modify `app.py`, restart Flask server to see changes
2. **Frontend Changes**: Edit `templates/index.html`, refresh browser (Flask serves static files)
3. **Memory Debugging**: Check `memory.db` for conversation storage, `chroma_data/` for vector embeddings
4. **API Key Management**: Never commit API keys; use `.env` file for local development

## File Structure Context

- **`app.py`**: Core Flask application with dual memory systems and Gemini integration
- **`templates/index.html`**: Complete chat interface with drag/drop, persistence, responsive design
- **`requirements.txt`**: Python dependencies (Flask, AI libraries, vector database)
- **`memory.db`**: SQLite database for conversation history
- **`chroma_data/`**: ChromaDB persistent storage for vector embeddings
- **`Rust_Project/`**: Separate Rust workspace (currently incomplete)

## Important Notes

- The application uses both structured (SQLite) and semantic (ChromaDB) memory but currently only leverages SQLite for conversation context
- ChromaDB integration is ready but unused - opportunity for semantic conversation enhancement
- Frontend includes localStorage backup for chat history persistence
- Gemini API key is hardcoded as fallback but should use environment variable
- User ID validation limits: 50 characters max, message limit: 1000 characters
- CORS is enabled for development; consider restrictions for production
