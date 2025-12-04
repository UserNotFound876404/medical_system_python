from flask import Flask, request, jsonify
import subprocess
import json
import os
from dotenv import load_dotenv
from typing import Final

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

    input_json = json.dumps({'question': question})
    print(f"Calling Python with: {question}")

    # Spawn chatbot.py with input_json argument
    process = subprocess.Popen(
        ['py', 'chatbot.py', input_json],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    stdout, stderr = process.communicate()

    print(f"Python process exited with code: {process.returncode}")
    print(f"STDOUT: {stdout.strip()}")
    print(f"STDERR: {stderr.strip()}")

    if process.returncode != 0:
        return jsonify({
            'error': f'Python script failed (exit code {process.returncode})',
            'stdout': stdout.strip(),
            'stderr': stderr.strip()
        }), 500

    try:
        response = json.loads(stdout.strip())
        return jsonify(response)
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}")
        return jsonify({
            'error': 'Failed to parse Python JSON response',
            'rawOutput': stdout.strip(),
            'stderr': stderr.strip()
        }), 500

@app.route('/health')
def health():
    return jsonify({'status': 'OK', 'port': PORT})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
