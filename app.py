from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import json
import logging
from datetime import datetime
from ai_handler import AIHandler

app = Flask(__name__, template_folder='templates')
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize AI Handler
ai_handler = AIHandler()

@app.route('/')
def index():
    """Serve the HTML chat interface"""
    return render_template('chat.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Main chat endpoint"""
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({
                'response': '⚠️ Invalid request format',
                'error': 'Missing message field'
            }), 400

        user_message = data['message'].strip()
        if not user_message:
            return jsonify({
                'response': '⚠️ Message cannot be empty',
                'error': 'Empty message'
            }), 400

        logger.info(f"Processing message: {user_message[:50]}...")

        # Process message
        result = ai_handler.process_message(user_message)

        # Log response
        logger.info(f"Response generated: {result.get('response', '')[:50]}...")

        return jsonify(result)

    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        return jsonify({
            'response': '⚠️ An error occurred while processing your request',
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'online',
        'timestamp': datetime.now().isoformat(),
        'version': 'v∞ OMNIBREAKER'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
