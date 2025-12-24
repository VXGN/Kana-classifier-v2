from flask import Flask, render_template, request, jsonify
import numpy as np
import cv2
import base64
import tensorflow as tf
import os

app = Flask(__name__)

# Model directory and available models
MODEL_DIR = os.path.join(os.path.dirname(__file__), 'model')

# Dictionary of available models with friendly names
AVAILABLE_MODELS = {
    'kana_classifier.h5': 'Default Model',
    'kana_classifier(augmented).h5': 'Augmented Model',
    'kana_classifier(the best).h5': 'Best Model'
}

# Current model state
current_model_name = 'kana_classifier.h5'
model = None

def load_model(model_name):
    """Load a model by filename"""
    global model, current_model_name
    model_path = os.path.join(MODEL_DIR, model_name)
    if os.path.exists(model_path):
        model = tf.keras.models.load_model(model_path)
        current_model_name = model_name
        return True
    return False

# Load default model on startup
load_model(current_model_name)

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

@app.route('/models')
def get_models():
    """Get list of available models"""
    models = []
    for filename, display_name in AVAILABLE_MODELS.items():
        model_path = os.path.join(MODEL_DIR, filename)
        if os.path.exists(model_path):
            models.append({
                'filename': filename,
                'display_name': display_name,
                'active': filename == current_model_name
            })
    return jsonify({'models': models, 'current': current_model_name})

@app.route('/switch_model', methods=['POST'])
def switch_model():
    """Switch to a different model"""
    try:
        data = request.get_json()
        model_name = data.get('model')
        
        if not model_name:
            return jsonify({'error': 'No model specified'}), 400
        
        if model_name not in AVAILABLE_MODELS:
            return jsonify({'error': 'Invalid model'}), 400
        
        if load_model(model_name):
            return jsonify({
                'success': True,
                'message': f'Switched to {AVAILABLE_MODELS[model_name]}',
                'current': model_name
            })
        else:
            return jsonify({'error': 'Failed to load model'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_ip():
    return os.popen("ipconfig").read().split("IPv4 Address")[-1].split(":")[1].split()[0]

if __name__ == '__main__':
    print("\n🎌 DoitsuKa - ドイツカ")
    print("Katakana Character Recognition")
    print("📱 Open: http://127.0.0.1:5000")
    print(f"IP (local network): http://{get_ip()}:5000")
    print("💡 Tip: Use 127.0.0.1 for camera permissions!\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
