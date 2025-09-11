import json
import os
from http.server import BaseHTTPRequestHandler
import google.generativeai as genai

# Configure Gemini AI
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-1.5-flash"

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Set CORS headers
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            # Read request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            user_id = data.get('user_id', 'guest')
            user_message = data.get('message', '')
            
            # Basic validation
            if not user_id or len(user_id) > 50:
                self.wfile.write(json.dumps({"error": "Invalid or missing user_id"}).encode())
                return
                
            if not user_message or len(user_message) > 1000:
                self.wfile.write(json.dumps({"error": "Invalid or missing message"}).encode())
                return
            
            # Build prompt (simplified - no persistent memory for Vercel)
            prompt = f"""
            You are Stan, a helpful and friendly AI assistant.
            
            The user is {user_id}.
            Now the user says: {user_message}
            
            Provide a helpful and engaging response. Be conversational and friendly.
            """
            
            # Generate response with Gemini
            model = genai.GenerativeModel(MODEL)
            response = model.generate_content(prompt)
            bot_reply = response.text.strip()
            
            # Return response
            result = {"reply": bot_reply}
            self.wfile.write(json.dumps(result).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            error_response = {"error": f"Internal server error: {str(e)}"}
            self.wfile.write(json.dumps(error_response).encode())
    
    def do_OPTIONS(self):
        # Handle preflight requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
