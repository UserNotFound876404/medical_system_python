from flask import Flask, request, jsonify
import subprocess
import json
import os
from dotenv import load_dotenv
from typing import Final
import chatbot

load_dotenv()
PORT: Final[str] = os.getenv('PORT')


app = Flask(__name__)

@app.route('/home')
def home():
    return "home", 200

@app.route('/ask')
def ask():
    question = request.args.get('q')
    if not question:
        return jsonify({'error': 'Missing ?q=question parameter'}), 400

    print(f"Calling chatbot with: {question}")

    response = chatbot.get_chatbot_response(question)
    print(f"Chatbot response: {response}")
    
    return jsonify(response)

@app.route('/health')
def health():
    return jsonify({'status': 'OK', 'port': PORT})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
