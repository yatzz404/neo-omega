import sys
import os

# Add parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from app import app
    print("✅ App imported successfully!")
except Exception as e:
    print(f"❌ Error importing app: {e}")
    # Fallback jika gagal
    from flask import Flask, jsonify
    app = Flask(__name__)
    
    @app.route('/')
    def index():
        return jsonify({
            'status': 'error',
            'message': 'Failed to load main app',
            'error': str(e)
        })
    
    @app.route('/api/health')
    def health():
        return jsonify({'status': 'degraded'})

# Vercel membutuhkan variable 'app'
# Sudah ada dari import di atas
