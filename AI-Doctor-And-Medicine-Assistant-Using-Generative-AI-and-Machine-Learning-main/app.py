import google.generativeai as genai
import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Set your Google API key
os.environ["GOOGLE_API_KEY"] = "you api here"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

model = genai.GenerativeModel("models/gemini-1.5-pro")

# Global variables to store conversation history and context
conversation_history = []

# Voice assistance function with enhanced medical focus
def voice_assistance(user_input):
    global conversation_history

    # Medical-specific prompt
    prompt = f"""
    You are a virtual AI Doctor. The user has shared the following symptoms or medical conditions:
    '{user_input}'
    Based on these symptoms, provide a concise response that includes possible conditions, suggested medications (if appropriate), lifestyle tips, and any precautionary advice. Your responses should be reassuring and professional, aimed at educating the user and guiding them on next steps.
    Avoid any unnecessary details or asking follow-up questions unless it would help the user's understanding. If the condition is serious, suggest consulting a healthcare provider.
    """

    response = model.generate_content(prompt).text

    # Update conversation history
    conversation_history.append({
        'user': user_input,
        'ai': response
    })

    return response

# Route to render the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle voice input and return model response with conversation history
@app.route('/process_voice', methods=['POST'])
def process_voice():
    user_input = request.json.get("user_input")
    response = voice_assistance(user_input)

    # Return the updated conversation history
    return jsonify({'response': response, 'conversation_history': conversation_history})

if __name__ == '__main__':
    app.run(debug=True)
