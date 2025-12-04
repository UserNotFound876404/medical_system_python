import cv2
import easyocr
import numpy as np
import json

def process_image(file_content: bytes) -> dict:
    """Process uploaded image bytes and return extracted text"""
    try:
        # Read image with OpenCV
        nparr = np.frombuffer(file_content, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            return {'success': False, 'error': 'Invalid image file'}
        
        # OCR with easyocr
        reader = easyocr.Reader(['en'], gpu=False)
        text_results = reader.readtext(img)
        
        # Sort text by position (top-left to bottom-right)
        sorted_text = sorted(text_results, key=lambda x: (x[0][0][1], x[0][0][0]))
        extracted_texts = [item[1] for item in sorted_text]
        full_text = ' '.join(extracted_texts)
        
        return {
            'success': True,
            'extracted_text': full_text,
            'words_count': len(extracted_texts),
            'raw_results': text_results
        }
    except Exception as e:
        return {'success': False, 'error': f'OCR processing failed: {str(e)}'}
