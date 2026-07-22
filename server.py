from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)

# ============================================================
# AI SEDERHANA (PAKE IF-ELSE)
# ============================================================

def jawab_ai(pesan):
    chat = pesan.lower()
    
    if "halo" in chat or "hai" in chat or "hey" in chat:
        return "Halo juga! Saya NEO-OMEGA, siap membantu anda."
    
    if "siapa" in chat and ("kamu" in chat or "nama" in chat):
        return "Saya NEO-OMEGA, AI buatan TUAN YATZZ."
    
    if "buat" in chat and "web server" in chat and "python" in chat:
        return '''Kode web server Flask:
from flask import Flask
app = Flask(__name__)
@app.route('/')
def home():
    return "NEO-OMEGA WEB SERVER"
app.run(host='0.0.0.0', port=5000)'''
    
    if "terima kasih" in chat or "makasih" in chat:
        return "Sama-sama! Senang bisa membantu."
    
    return "Maaf, saya masih belajar. Coba tanya: 'halo', 'siapa kamu', atau 'buat web server pake python'."

# ============================================================
# ROUTE
# ============================================================

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    pesan = data.get('message', '').strip()
    
    if not pesan:
        return jsonify({'response': 'Tulis sesuatu!'})
    
    balasan = jawab_ai(pesan)
    
    return jsonify({
        'response': balasan,
        'code': '',
        'output': ''
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
