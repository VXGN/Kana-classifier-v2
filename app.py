"""
DoitsuKa - ドイツカ
A Katakana Character Recognition Web App
Doitsu No Kana? (Which Kana is it?)
"""

from flask import Flask, render_template, request, jsonify
import numpy as np
import cv2
import base64
import tensorflow as tf
import os

app = Flask(__name__)

# Load the trained model
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model', 'kana_classifier.h5')
model = tf.keras.models.load_model(MODEL_PATH)

# Katakana categories
CATEGORIES = [
    {'romaji': 'shi', 'kana': 'シ'},
    {'romaji': 'tsu', 'kana': 'ツ'},
    {'romaji': 'n', 'kana': 'ン'},
    {'romaji': 'so', 'kana': 'ソ'},
    {'romaji': 'no', 'kana': 'ノ'},
    {'romaji': 'me', 'kana': 'メ'},
]

def preprocess_image(image_data):
    """Preprocess image exactly like training pipeline"""
    img_bytes = base64.b64decode(image_data.split(',')[1])
    img_array = np.frombuffer(img_bytes, dtype=np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (64, 64))
    bilateral = cv2.bilateralFilter(resized.astype(np.uint8), 5, sigmaColor=28, sigmaSpace=25)
    processed = bilateral.reshape(1, 64, 64, 1)
    
    # Encode preprocessed image for display
    _, buffer = cv2.imencode('.png', bilateral)
    preprocessed_base64 = base64.b64encode(buffer).decode('utf-8')
    preprocessed_data_url = f'data:image/png;base64,{preprocessed_base64}'
    
    return processed, preprocessed_data_url

@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html', categories=CATEGORIES)

@app.route('/predict', methods=['POST'])
def predict():
    """Predict katakana from image"""
    try:
        data = request.get_json()
        image_data = data.get('image')
        
        if not image_data:
            return jsonify({'error': 'No image data provided'}), 400
        
        processed, preprocessed_img = preprocess_image(image_data)
        predictions = model.predict(processed, verbose=0)[0]
        
        results = []
        for i, conf in enumerate(predictions):
            results.append({
                'romaji': CATEGORIES[i]['romaji'],
                'kana': CATEGORIES[i]['kana'],
                'confidence': float(conf) * 100
            })
        
        results.sort(key=lambda x: x['confidence'], reverse=True)
        
        return jsonify({
            'success': True,
            'predictions': results,
            'top_prediction': results[0],
            'preprocessed_image': preprocessed_img
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'model_loaded': model is not None})

if __name__ == '__main__':
    print("\n🎌 DoitsuKa - ドイツカ")
    print("Katakana Character Recognition")
    print("📱 Open: http://127.0.0.1:5000")
    print("💡 Tip: Use 127.0.0.1 for camera permissions!\n")
    app.run(debug=True, host='127.0.0.1', port=5000)
