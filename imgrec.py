# imgrec.py - Azure-safe version
import cv2
import numpy as np
import base64
import io
from PIL import Image
import pytesseract

def process_image(file_content: bytes) -> dict:
    try:
        # Read image with OpenCV
        nparr = np.frombuffer(file_content, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            return {'success': False, 'error': 'Invalid image file'}
        
        # Convert to PIL Image for Tesseract
        img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        
        # OCR with pytesseract (lightweight)
        extracted_text = pytesseract.image_to_string(img_pil)
        
        words = extracted_text.split()
        words_count = len(words)
        
        return {
            'success': True,
            'extracted_text': extracted_text.strip(),
            'words_count': words_count,
            'image_size': f"{img.shape[1]}x{img.shape[0]}"
        }
        
    except Exception as e:
        return {'success': False, 'error': str(e)}
