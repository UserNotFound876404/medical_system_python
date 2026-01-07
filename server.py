from flask import Flask, request, jsonify,render_template
import json
import os
from dotenv import load_dotenv
from typing import Final
import chatbot
# import imgrec 

load_dotenv()
PORT: Final[str] = os.getenv('PORT')


app = Flask(__name__)


@app.route('/')
def home():
    return "home", 200

@app.route('/ask',methods=['POST'])
def ask():
    data = request.get_json()
    if not data or not data.get('q'):
        return jsonify({'error': 'Missing question variable'}), 400

    question = data['q']
    print(f"Calling chatbot with: {data}")

    response = chatbot.get_chatbot_response(question)
    print(f"Chatbot response: {response}")
    
    return jsonify(response)

#curl -X POST http://localhost:8099/ask -H "Content-Type: application/json" -d "{\"q\": \"Hello chatbot\"}"
#text reconizer
'''
@app.route('/imgrec', methods=['GET', 'POST'])
def imgrec_route():  
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
'''
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
