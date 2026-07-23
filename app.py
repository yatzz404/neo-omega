from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import sys
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inisialisasi Flask
app = Flask(__name__, template_folder='templates')
CORS(app)

# Import AI Handler dengan error handling
try:
    from ai_handler import AIHandler
    ai_handler = AIHandler()
    logger.info("✅ AI Handler loaded successfully!")
except Exception as e:
    logger.error(f"❌ Failed to load AI Handler: {e}")
    ai_handler = None

@app.route('/')
def index():
    try:
        return render_template('chat.html')
    except Exception as e:
        return f"Error loading chat.html: {e}"

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        if ai_handler is None:
            return jsonify({
                'response': '⚠️ AI Handler not loaded. Please check logs.',
                'error': 'AI Handler not initialized'
            }), 500

        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({
                'response': '⚠️ Invalid request',
                'error': 'Missing message'
            }), 400

        user_message = data['message'].strip()
        if not user_message:
            return jsonify({
                'response': '⚠️ Message cannot be empty',
                'error': 'Empty message'
            }), 400

        logger.info(f"Processing: {user_message[:50]}...")
        result = ai_handler.process_message(user_message)
        return jsonify(result)

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({
            'response': f'⚠️ Error: {str(e)}',
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'online' if ai_handler else 'degraded',
        'timestamp': datetime.now().isoformat(),
        'version': 'v∞ OMNIBREAKER',
        'ai_loaded': ai_handler is not None
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
