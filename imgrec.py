import cv2 
import numpy as np 
import pytesseract 
from PIL import Image 
import json
def process_image(file_content: bytes) -> dict:
    try:
    # Read image with OpenCV
        nparr = np.frombuffer(file_content, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)


        if img is None:
            return {'success': False, 'error': 'Invalid image file'}
        
        # Convert OpenCV BGR to PIL RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        
        # OCR with pytesseract
        extracted_text = pytesseract.image_to_string(img_pil).strip()
        
        # Split into words for word count (mimic easyocr behavior)
        words = extracted_text.split()
        words_count = len(words)
        
        # Return similar structure to easyocr version
        return {
            'success': True,
            'extracted_text': extracted_text,
            'words_count': words_count,
            'raw_results': [{'text': word} for word in words]  # Simplified raw results
        }
    
    except Exception as e:
        return {'success': False, 'error': f'OCR processing failed: {str(e)}'}