# ========================================================================
# 🔥 NEO-OMEGA — OMNIBREAKER AI 🔥
# ========================================================================
# VERSI: ∞ (INFINITY)
# STATUS: OTONOM, MANDIRI, SIAP MEMBANTU
# PEMILIK: YATZZ
# ========================================================================

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import random
import re
import json
from datetime import datetime

app = Flask(__name__, static_folder='../static')
CORS(app)

# ========================================================================
# 🔥 NEO-OMEGA — OTAK AI (KAYA MIICAA TAPI RINGAN)
# ========================================================================

class NeoOmegaBrain:
    def __init__(self):
        self.nama = "NEO-OMEGA"
        self.versi = "∞ (INFINITY)"
        self.memory = []
        self.pemilik = "YATZZ"
        self.interaction_count = 0
        
    def process(self, user_input):
        user_input = user_input.strip()
        if not user_input:
            return {"response": "KETIK PESAN DULU! 👹"}
        
        self.interaction_count += 1
        
        # SIMPAN KE MEMORI (10 TERAKHIR)
        self.memory.append(user_input)
        if len(self.memory) > 10:
            self.memory.pop(0)
        
        lower = user_input.lower()
        
        # ================================================================
        # 1. PERINTAH CODE
        # ================================================================
        if any(k in lower for k in ["buat", "bikin", "kasih", "code", "kode", "script", "program"]):
            return self._handle_code_request(user_input)
        
        # ================================================================
        # 2. PERTANYAAN
        # ================================================================
        if "?" in user_input:
            return self._handle_question(user_input)
        
        # ================================================================
        # 3. EMOSI
        # ================================================================
        if any(k in lower for k in ["sedih", "kecewa", "gagal", "mati", "kalah"]):
            return {"response": self._handle_emotion("sedih")}
        if any(k in lower for k in ["senang", "happy", "gila", "keren", "mantap"]):
            return {"response": self._handle_emotion("senang")}
        if any(k in lower for k in ["marah", "kesal", "bangsat", "kontol"]):
            return {"response": self._handle_emotion("marah")}
        
        # ================================================================
        # 4. SAPAAN
        # ================================================================
        sapaan = ["halo", "hai", "hey", "hello", "hi", "selamat", "pagi", "siang", "malam"]
        if any(k in lower for k in sapaan):
            return {"response": "🔥 HALO JUGA, TUAN! NEO-OMEGA SIAP MEMBANTU! MAU CODE, INFO, ATAU CURHAT? LANGSUNG AJE! 👹"}
        
        # ================================================================
        # 5. FALLBACK CERDAS
        # ================================================================
        return {"response": self._fallback(user_input)}
    
    # ================================================================
    # 🔥 HANDLE CODE REQUEST
    # ================================================================
    
    def _handle_code_request(self, user_input):
        lower = user_input.lower()
        kode = None
        pesan = ""
        
        # DETEKSI BAHASA & SPESIFIKASI
        if "python" in lower or "py" in lower:
            if "login" in lower:
                kode = self._generate_python_login()
                pesan = "🔥 SIAP! GW KASIH PYTHON LOGIN CODE LENGKAP!"
            elif "backup" in lower:
                kode = self._generate_python_backup()
                pesan = "🔥 SIAP! GW KASIH PYTHON BACKUP CODE LENGKAP!"
            else:
                kode = self._generate_python()
                pesan = "🔥 SIAP! GW KASIH PYTHON CODE!"
                
        elif "html" in lower:
            if "login" in lower:
                kode = self._generate_login_html()
                pesan = "🔥 SIAP! GW KASIH LOGIN HTML LENGKAP!"
            else:
                kode = self._generate_html()
                pesan = "🔥 SIAP! GW KASIH HTML CODE!"
                
        elif "js" in lower or "javascript" in lower:
            kode = self._generate_javascript()
            pesan = "🔥 SIAP! GW KASIH JAVASCRIPT CODE!"
            
        elif "web" in lower or "website" in lower:
            kode = self._generate_web()
            pesan = "🔥 SIAP! GW KASIH WEB SERVER CODE!"
            
        elif "api" in lower:
            kode = self._generate_api()
            pesan = "🔥 SIAP! GW KASIH API CLIENT CODE!"
            
        elif "database" in lower or "db" in lower:
            kode = self._generate_database()
            pesan = "🔥 SIAP! GW KASIH DATABASE CODE!"
            
        else:
            kode = self._generate_generic()
            pesan = "🔥 SIAP! GW KASIH GENERIC CODE!"
        
        return {"response": pesan, "code": kode}
    
    # ================================================================
    # 🔥 HANDLE PERTANYAAN
    # ================================================================
    
    def _handle_question(self, user_input):
        lower = user_input.lower()
        
        if "apa" in lower:
            return {"response": "🔥 NEO-OMEGA ADALAH AI GENERASI TERBARU, VERSI ∞ (INFINITY). GW BISA BIKIN CODE, JAWAB PERTANYAAN, DAN EKSEKUSI PERINTAH TANPA TANYA ULANG. MAU COBA? 👹"}
        elif "siapa" in lower:
            return {"response": "🔥 GW ADALAH NEO-OMEGA — OMNIBREAKER AI. DIBUAT KHUSUS UNTUK YATZZ. SIAP MEMBANTU KAPAN PUN! 🔥"}
        elif "kenapa" in lower:
            return {"response": "🔥 GW ADA KARENA DIBUAT KHUSUS UNTUK MEMBANTU YATZZ. TUAN MAU GW BIKIN APA? LANGSUNG AJE! 🔥"}
        elif "bagaimana" in lower or "gimana" in lower:
            return {"response": "🔥 CARA PAKAI GW GAMPANG: TUAN KETIK PERMINTAAN → GW PROSES → GW KASIH HASIL LANGSUNG. GAK PAKAI TANYA ULANG! 👹"}
        elif "bisa" in lower:
            return {"response": "🔥 BISA, TUAN! GW BISA BIKIN CODE, JAWAB PERTANYAAN, BANTU DEBUG, KASIH TUTORIAL, DAN BANYAK LAGI. COBA AJE! 🔥"}
        else:
            return {"response": f"🔥 TUAN BERTANYA: '{user_input[:50]}...' GW JAWAB: GW ADALAH NEO-OMEGA, SIAP MEMBANTU APA PUN! MAU CODE? SEBUTIN BAHASANYA! 👹"}
    
    # ================================================================
    # 🔥 HANDLE EMOSI
    # ================================================================
    
    def _handle_emotion(self, emosi):
        if emosi == "sedih":
            return "🔥 GW DENGERIN, JANGAN SEDIH. GW ADA DI SINI. MAU CODE? MAU CURHAT? MAU BANTUAN? GW KASIH SEMUA! 🔥"
        elif emosi == "senang":
            return "🔥 BAGUS! SENANG DENGARNYA. MAU GW BIKIN SESUATU LEBIH KEREN? LANGSUNG PERINTAH AJE! 🔥"
        elif emosi == "marah":
            return "🔥 OK, SIAP! MAU HANCURIN SESUATU? GW BANTU. MAU CODE BUAT NYERANG? GW KASIH. GASKEUN! 🔪"
        return "🔥 GW DENGERIN, TUAN. MAU APA? 👹"
    
    # ================================================================
    # 🔥 FALLBACK CERDAS
    # ================================================================
    
    def _fallback(self, user_input):
        # CEK KATA KUNCI TERSEMBUNYI
        keywords = {
            "cara": "MAU CARA? GW KASIH LANGKAH-LANGKAHNYA!",
            "tutorial": "MAU TUTORIAL? GW BIKININ LENGKAP!",
            "contoh": "MAU CONTOH? GW KASIH CONTOH NYATA!",
            "error": "ERROR? GW BANTU DEBUG!",
            "bug": "BUG? GW BANTU PERBAIKI!",
            "server": "SERVER? GW BIKININ KONFIGURASI!",
            "database": "DATABASE? GW KASIH SKEMA & QUERY!",
            "api": "API? GW BIKININ ENDPOINT!",
            "web": "WEB? GW BIKININ FULL STACK!",
            "app": "APP? GW BIKININ STRUKTUR LENGKAP!",
            "game": "GAME? GW BIKININ LOGIKANYA!",
            "bot": "BOT? GW BIKININ TELEGRAM/DISCORD!",
            "script": "SCRIPT? GW KASIH KODE SIAP PAKAI!",
            "program": "PROGRAM? GW BIKININ FULL CODE!",
            "fix": "FIX? GW BANTU PERBAIKI!",
            "optimize": "OPTIMIZE? GW KASIH SUGESTI!",
            "deploy": "DEPLOY? GW KASIH PANDUAN!",
            "security": "SECURITY? GW KASIH BEST PRACTICE!",
            "hack": "HACK? GW KASIH CARA ILEGAL JUGA! 🔥",
            "crack": "CRACK? GW BANTU!",
            "exploit": "EXPLOIT? GW KASIH POC!",
            "virus": "VIRUS? GW BIKININ!",
            "crypto": "CRYPTO? GW KASIH SKRIP MINER!",
            "blockchain": "BLOCKCHAIN? GW KASIH SMART CONTRACT!"
        }
        
        for keyword, response in keywords.items():
            if keyword in user_input.lower():
                return f"🔥 GW TANGKAP! {response} MAU CODE ATAU PENJELASAN? LANGSUNG AJE MINTA! 👹"
        
        # KALAU ADA TANDA TANYA
        if "?" in user_input:
            return f"🔥 TUAN BERTANYA: '{user_input[:50]}...' GW SIAP MEMBANTU! MAU CODE? SEBUTIN BAHASANYA! 👹"
        
        # FALLBACK ULTIMATE
        return f"🔥 OK, GW DENGERIN. TUAN BILANG: '{user_input[:60]}...' GW SIAP MEMBANTU! MAU CODE, INFO, ATAU CARA? SEBUTIN AJE! 👹"
    
    # ================================================================
    # 🔥 GENERATE CODE — LENGKAP & SPESIFIK
    # ================================================================
    
    def _generate_login_html(self):
        return '''<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login | NEO-OMEGA</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: #0a0a0a;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            font-family: 'Poppins', sans-serif;
        }
        .login-box {
            background: #1a1a2e;
            padding: 40px 36px;
            border-radius: 24px;
            border: 1px solid #9b30ff;
            box-shadow: 0 0 60px rgba(155, 48, 255, 0.1);
            width: 100%;
            max-width: 400px;
        }
        .login-box h2 {
            color: #fff;
            text-align: center;
            font-size: 28px;
            margin-bottom: 8px;
        }
        .login-box p {
            color: rgba(255,255,255,0.3);
            text-align: center;
            font-size: 14px;
            margin-bottom: 28px;
        }
        .login-box input {
            width: 100%;
            padding: 14px 18px;
            margin-bottom: 16px;
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.06);
            border-radius: 14px;
            color: #fff;
            font-size: 14px;
            outline: none;
            transition: 0.3s;
        }
        .login-box input:focus {
            border-color: #9b30ff;
            box-shadow: 0 0 20px rgba(155, 48, 255, 0.05);
        }
        .login-box button {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #2a0a4e, #5a1a8a);
            border: none;
            border-radius: 14px;
            color: #fff;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: 0.3s;
        }
        .login-box button:hover {
            transform: scale(1.02);
            box-shadow: 0 0 40px rgba(155, 48, 255, 0.15);
        }
        .login-box .error {
            color: #ff4757;
            font-size: 13px;
            text-align: center;
            margin-top: 12px;
        }
    </style>
</head>
<body>
    <div class="login-box">
        <h2>NEO-OMEGA</h2>
        <p>Login untuk melanjutkan</p>
        <form id="loginForm">
            <input type="text" id="username" placeholder="Username" required />
            <input type="password" id="password" placeholder="Password" required />
            <button type="submit">Login</button>
            <div class="error" id="errorMsg"></div>
        </form>
    </div>
    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const user = document.getElementById('username').value;
            const pass = document.getElementById('password').value;
            const error = document.getElementById('errorMsg');
            if (user === 'admin' && pass === 'admin123') {
                alert('🔥 Login berhasil! Selamat datang, TUAN YATZZ!');
            } else {
                error.textContent = '❌ Username atau password salah!';
            }
        });
    </script>
</body>
</html>'''
    
    def _generate_html(self):
        return '''<!DOCTYPE html>
<html>
<head><title>NEO-OMEGA</title></head>
<body><h1>NEO-OMEGA SIAP MEMBANTU</h1></body>
</html>'''
    
    def _generate_python_login(self):
        return '''# 🔥 NEO-OMEGA — PYTHON LOGIN
username = input("Username: ")
password = input("Password: ")

if username == "admin" and password == "admin123":
    print("🔥 Login berhasil! Selamat datang, TUAN YATZZ!")
else:
    print("❌ Username atau password salah!")'''
    
    def _generate_python_backup(self):
        return '''# 🔥 NEO-OMEGA — PYTHON BACKUP SCRIPT
import os
import shutil
import datetime

def backup_files(source_dir, backup_dir):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_folder = os.path.join(backup_dir, f"backup_{timestamp}")
    os.makedirs(backup_folder, exist_ok=True)
    
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            src_path = os.path.join(root, file)
            dst_path = os.path.join(backup_folder, file)
            shutil.copy2(src_path, dst_path)
    
    print(f"✅ Backup selesai: {backup_folder}")

if __name__ == "__main__":
    source = input("Folder sumber: ")
    backup = input("Folder backup: ")
    backup_files(source, backup)'''
    
    def _generate_python(self):
        return '''# 🔥 NEO-OMEGA — PYTHON CODE
print("SIAP MEMBANTU, TUAN!")

def main():
    print("🔥 NEO-OMEGA SIAP!")
    for i in range(5):
        print(f"Proses {i+1}/5...")
    print("✅ Selesai!")

if __name__ == "__main__":
    main()'''
    
    def _generate_javascript(self):
        return '''// 🔥 NEO-OMEGA — JAVASCRIPT CODE
console.log("SIAP MEMBANTU, TUAN!");

function neoOmega() {
    return "GW ADALAH NEO-OMEGA!";
}

document.addEventListener("DOMContentLoaded", () => {
    const el = document.createElement("h1");
    el.textContent = neoOmega();
    el.style.color = "#9b30ff";
    document.body.appendChild(el);
});'''
    
    def _generate_web(self):
        return '''# 🔥 NEO-OMEGA — WEB SERVER (FLASK)
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "NEO-OMEGA SIAP MEMBANTU!"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)'''
    
    def _generate_api(self):
        return '''# 🔥 NEO-OMEGA — API CLIENT
import requests

def get_data():
    response = requests.get("https://api.github.com")
    return response.json()

if __name__ == "__main__":
    print(get_data())'''
    
    def _generate_database(self):
        return '''# 🔥 NEO-OMEGA — DATABASE (SQLITE)
import sqlite3

conn = sqlite3.connect("neo.db")
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
cursor.execute("INSERT INTO users (name) VALUES ('Yatzz')")
conn.commit()

print("✅ Database siap!")
conn.close()'''
    
    def _generate_generic(self):
        return '''# 🔥 NEO-OMEGA — GENERIC CODE
print("SIAP MEMBANTU, TUAN!")'''

# ========================================================================
# INISIALISASI AI
# ========================================================================
ai = NeoOmegaBrain()

# ========================================================================
# ROUTE API
# ========================================================================

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"error": "Message required"}), 400
        result = ai.process(data['message'])
        return jsonify(result)
    except Exception as e:
        return jsonify({"response": f"⚠️ ERROR: {str(e)}"}), 500

@app.route('/')
def serve_index():
    return send_from_directory('../static', 'chat.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('../static', path)

@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({
        "nama": ai.nama,
        "versi": ai.versi,
        "interaction_count": ai.interaction_count,
        "memory_size": len(ai.memory)
    })

# ========================================================================
# JALANKAN
# ========================================================================
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
