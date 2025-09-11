from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3
import google.generativeai as genai
import os
import chromadb
from sentence_transformers import SentenceTransformer
from contextlib import contextmanager
import logging
from dotenv import load_dotenv
import socket

socket.setdefaulttimeout(30)
socket.AF_INET
load_dotenv()


# ---- Config ----
app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

genai.configure(api_key=os.getenv("GEMINI_API_KEY","AIzaSyAkwgcEJsxAvpv-0JRdYOTe74q9Idz9-Yc"))
if not os.getenv("GEMINI_API_KEY"):
    raise ValueError("GEMINI_API_KEY environment variable not set")
MODEL = "gemini-1.5-flash"

# ---- SQLite Setup (facts) ----
@contextmanager
def get_db_connection():
    conn = sqlite3.connect("memory.db", check_same_thread=False)
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    try:
        with get_db_connection() as conn:
            c = conn.cursor()
            c.execute("""CREATE TABLE IF NOT EXISTS memory (
                        user_id TEXT,
                        key TEXT,
                        value TEXT
                    )""")
            conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Database initialization error: {e}")

init_db()

def save_memory(user_id, key, value):
    try:
        with get_db_connection() as conn:
            c = conn.cursor()
            c.execute("INSERT INTO memory (user_id, key, value) VALUES (?, ?, ?)", (user_id, key, value))
            conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Database save error: {e}")
        return False
    return True

def get_memory(user_id):
    try:
        with get_db_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT key, value FROM memory WHERE user_id=?", (user_id,))
            data = c.fetchall()
            return {k: v for k, v in data}
    except sqlite3.Error as e:
        logger.error(f"Database retrieval error: {e}")
        return {}

# ---- ChromaDB Setup (semantic memory) ----
chroma_client = chromadb.PersistentClient(path="./chroma_data")
collection = chroma_client.get_or_create_collection("chat_memory")
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

def save_vector_memory(user_id, text):
    try:
        embedding = embed_model.encode([text])[0].tolist()
        collection.add(
            documents=[text],
            embeddings=[embedding],
            metadatas=[{"user": user_id}],
            ids=[f"{user_id}_{abs(hash(text))}"]
        )
    except Exception as e:
        logger.error(f"ChromaDB save error: {e}")

def recall_vector_memory(user_id, query, n_results=5, min_similarity=0.3):
    try:
        embedding = embed_model.encode([query])[0].tolist()
        results = collection.query(
            query_embeddings=[embedding],
            n_results=n_results,
            where={"user": user_id}
        )
        if results.get("distances"):
            filtered_docs = [
                doc for doc, dist in zip(results["documents"][0], results["distances"][0])
                if dist < (1 - min_similarity)  # Assuming cosine similarity
            ]
            return filtered_docs
        return results["documents"][0] if results["documents"] else []
    except Exception as e:
        logger.error(f"ChromaDB query error: {e}")
        return []


# ---- Routes ----
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_id = data.get("user_id", "guest")
    user_message = data.get("message", "")

    if not user_id or len(user_id) > 50:
        return jsonify({"error": "Invalid or missing user_id"}), 400
    if not user_message or len(user_message) > 1000:
        return jsonify({"error": "Invalid or missing message"}), 400

    try:
        # 1. Retrieve memory (previous user messages + bot replies)
        with get_db_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT value FROM memory WHERE user_id=?", (user_id,))
            rows = c.fetchall()
        past_memories = [r[0] for r in rows] if rows else []

        # Keep only last 5 interactions for context
        memory_context = "\n".join(past_memories[-5:])

        # 2. Build prompt with memory
        prompt = f"""
        You are Stan, a helpful and friendly assistant.

        The user is {user_id}.
        In previous chats, the user has shared these details and preferences:
        {memory_context if memory_context else "None yet"}

        Now the user says: {user_message}

        Use their past preferences when possible to personalize your response.
        """

        # 3. Send prompt to Gemini
        model = genai.GenerativeModel(MODEL)
        response = model.generate_content(prompt)
        bot_reply = response.text.strip()

        # 4. Save user message + bot reply into memory
        with get_db_connection() as conn:
            c = conn.cursor()
            c.execute("INSERT INTO memory (user_id, key, value) VALUES (?, ?, ?)",
                      (user_id, "user_message", user_message))
            c.execute("INSERT INTO memory (user_id, key, value) VALUES (?, ?, ?)",
                      (user_id, "bot_reply", bot_reply))
            conn.commit()

        return jsonify({"reply": bot_reply})

    except Exception as e:
        logger.error(f"Chat endpoint error: {e}")
        return jsonify({"error": "Internal server error"}), 500


# ---- Run ----
if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)