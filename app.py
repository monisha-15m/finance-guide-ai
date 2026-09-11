import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai
from chatbot_config import SYSTEM_PROMPT

load_dotenv()
app = Flask(__name__)

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    if not message:
        return jsonify({"reply": "Please enter a question."}), 400
    if not client:
        return jsonify({"reply": "Gemini API key is not configured yet."}), 500
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=SYSTEM_PROMPT + "\n\nUser question:\n" + message
        )
        return jsonify({"reply": getattr(response, "text", None) or "I could not generate a response."})
    except Exception:
        return jsonify({"reply": "Sorry, I could not process your request right now."}), 500

if __name__ == "__main__":
    app.run()
