from flask import Flask, request, jsonify,render_template
import json
import os
from dotenv import load_dotenv
from typing import Final
import chatbot

load_dotenv()
PORT: Final[str] = os.getenv('PORT')


app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('home'))

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

#text reconizer
@app.route('/imgrec', methods=['GET', 'POST'])
def imgrec_route():  # Your existing route ✅
    if request.method == 'POST':
        # Check if file uploaded
        if 'image' not in request.files:
            return render_template('imgrec.html', error='No image file provided')
        
        file = request.files['image']
        if file.filename == '':
            return render_template('imgrec.html', error='No image selected')
        
        # Validate image extension
        if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            return render_template('imgrec.html', error='Invalid image format (JPG/PNG)')
        
        # ✅ Call your imgrec.py function
        result = imgrec.process_image(file.read())
        return render_template('imgrec.html', **result)
    
    # GET - show form
    return render_template('imgrec.html')  # ✅ Clean - no variables!
    

@app.route('/health')
def health():
    return jsonify({'status': 'OK', 'port': PORT})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)



