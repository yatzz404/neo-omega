import sys
import os

# Tambahkan root directory ke path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from app import app as application
    print("✅ App imported successfully!")
except Exception as e:
    print(f"❌ Error importing app: {e}")
    # Fallback app
    from flask import Flask, jsonify
    application = Flask(__name__)
    
    @application.route('/')
    def index():
        return jsonify({
            'status': 'error',
            'message': 'Failed to load main app',
            'error': str(e)
        })
    
    @application.route('/api/health')
    def health():
        return jsonify({
            'status': 'degraded',
            'error': str(e)
        })

# Vercel membutuhkan 'app'
app = application
