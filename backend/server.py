import os
import sys
import json

from flask import Flask, request, jsonify, render_template, Response

# -------------------------------------------------
# Add project root to Python path
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from controller import Controller
from voice.voice_manager import VoiceManager  # ✅ NEW

# -------------------------------------------------
# Flask App Setup
# -------------------------------------------------
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "frontend", "templates"),
    static_folder=os.path.join(BASE_DIR, "frontend", "static"),
)

controller = Controller()
voice_manager = VoiceManager()  # ✅ NEW (Safe global instance)

# -------------------------------------------------
# Routes
# -------------------------------------------------


@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------------------
# Non-Streaming (Fallback)
# -----------------------------------------
@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    response = controller.process_input(user_input)
    return jsonify({"response": response})


# -----------------------------------------
# Streaming (Server-Sent Events)
# -----------------------------------------
@app.route("/chat-stream", methods=["POST"])
def chat_stream():
    user_input = request.json.get("message")

    def generate():
        try:
            for token in controller.stream_input(user_input):
                payload = json.dumps({"token": token})
                yield f"data: {payload}\n\n"

            yield "data: [DONE]\n\n"

        except Exception as e:
            error_payload = json.dumps({"error": str(e)})
            yield f"data: {error_payload}\n\n"
            yield "data: [DONE]\n\n"

    return Response(
        generate(),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


# -----------------------------------------
# 🎤 Voice Chat (NEW SAFE ROUTE)
# -----------------------------------------
@app.route("/voice-chat", methods=["POST"])
def voice_chat():
    try:
        # 1️⃣ Listen and Transcribe
        user_text = voice_manager.listen()

        if not user_text:
            return jsonify({"error": "No speech detected."}), 400

        # 2️⃣ Send to Controller
        response_text = controller.process_input(user_text)

        # 3️⃣ Speak the response
        voice_manager.speak(response_text)

        return jsonify({"user_text": user_text, "response": response_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True, threaded=True)
