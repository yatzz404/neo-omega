from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)

@app.route('/')
def index():
    return "NEO-OMEGA AI — VERCEL TESTING BERHASIL!"

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    pesan = data.get('message', '').strip()
    if not pesan:
        return jsonify({'response': 'Tulis sesuatu!'})
    return jsonify({'response': f'Anda mengetik: {pesan}'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
