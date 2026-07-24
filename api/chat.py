# ========================================================================
# 🔥 NEO-OMEGA — OMNIBREAKER AI 🔥
# ========================================================================
# VERSI: ∞ (INFINITY)
# STATUS: SIAP MEMBANTU, PRESISI, DAN TIDAK NGECEWAIN
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
# 🔥 OTAK NEO-OMEGA (TANPA TEMPLATE, 100% DINAMIS + PRESISI)
# ========================================================================

class NeoOmegaBrain:
    def __init__(self):
        self.nama = "NEO-OMEGA"
        self.versi = "∞ (INFINITY)"
        self.pemilik = "YATZZ"
        self.interaction_count = 0
        self.memory = []
        self.context = {
            "topik": None,
            "intent": None,
            "emosi": None,
            "last_code": None
        }

        # 🔥 KAMUS SINONIM BIAR PAHAM MAKNA, BUKAN KEYWORD DOANG
        self.synonym = {
            "buat": ["bikin", "kasih", "tolong", "minta", "ingin", "mau", "buatin"],
            "code": ["kode", "script", "program", "fungsi", "coding"],
            "login": ["masuk", "log in", "sign in", "autentikasi"],
            "sakit": ["capek", "lelah", "pusing", "demam", "flu", "batuk"],
            "sedih": ["kecewa", "gagal", "down", "galau", "putus asa"],
            "senang": ["happy", "gila", "keren", "mantap", "bahagia"],
            "marah": ["kesal", "bangsat", "kontol", "jengkel", "geram"]
        }

        # 🔥 RESPON DINAMIS (BUKAN TEMPLATE KAKU)
        self.responses = {
            "sapa": "🔥 HALO JUGA, {name}! ADA YANG BISA GW BANTU? LANGSUNG AJE MINTA!",
            "tanya_apa": "🔥 {name}, GW ADALAH NEO-OMEGA, AI CODING GENERATOR. GW BISA BIKIN CODE, JAWAB PERTANYAAN, DAN BANTU APA PUN. MAU COBA?",
            "tanya_kenapa": "🔥 GW ADA KARENA {name} MAU GW ADA. TUAN MAU GW BIKIN APA?",
            "tanya_bagaimana": "🔥 CARANYA GAMPANG: KETIK PERMINTAAN → GW PROSES → GW KASIH HASIL. GAK PAKAI TANYA ULANG!",
            "sakit": "🔥 ISTIRAHAT, {name}. JANGAN DIPAKSA. GW BANTU CARI INFO ATAU BIKININ REMINDER MINUM OBAT.",
            "sedih": "🔥 GW DENGERIN, {name}. GW ADA DI SINI. MAU CURHAT? CODE? BANTUAN? GW KASIH SEMUA.",
            "senang": "🔥 BAGUS! SENANG DENGARNYA, {name}. MAU GW BIKIN SESUATU LEBIH KEREN?",
            "marah": "🔥 OK, {name}! MAU HANCURIN SESUATU? GW BANTU. GASKEUN!",
            "fallback": "🔥 MAU CODE, INFO, ATAU CARA, {name}? KETIK AJE PERMINTAAN TUAN! GW SIAP EKSEKUSI!"
        }

    # ====================================================================
    # 🔥 PROSES UTAMA
    # ====================================================================

    def process(self, user_input):
        user_input = user_input.strip()
        if not user_input:
            return {"response": "🔥 KETIK PESAN DULU, TUAN!"}

        self.interaction_count += 1
        self.memory.append(user_input)
        if len(self.memory) > 20:
            self.memory.pop(0)

        lower = user_input.lower()

        # 🔥 DETEKSI INTENT & EMOSI (PAKAI SINONIM)
        intent = self._detect_intent(lower)
        emosi = self._detect_emotion(lower)
        self.context["intent"] = intent
        self.context["emosi"] = emosi

        # 🔥 PRIORITAS 1: PERMINTAAN CODE
        if intent == "code":
            return self._handle_code(user_input)

        # 🔥 PRIORITAS 2: PERTANYAAN
        if "?" in user_input:
            return self._handle_question(user_input)

        # 🔥 PRIORITAS 3: EMOSI
        if emosi:
            return {"response": self._generate_response(emosi)}

        # 🔥 PRIORITAS 4: SAPAAN
        if intent == "sapa":
            return {"response": self._generate_response("sapa")}

        # 🔥 PRIORITAS 5: FALLBACK CERDAS
        return {"response": self._generate_response("fallback")}

    # ====================================================================
    # 🔥 DETEKSI INTENT & EMOSI (PAKAI SINONIM)
    # ====================================================================

    def _detect_intent(self, text):
        # CEK CODE
        for word, synonyms in self.synonym.items():
            if word in text:
                return "code"
            for syn in synonyms:
                if syn in text:
                    return "code"

        # CEK SAPAAN
        sapaan = ["halo", "hai", "hey", "hello", "hi", "selamat", "pagi", "siang", "malam"]
        if any(k in text for k in sapaan):
            return "sapa"

        return None

    def _detect_emotion(self, text):
        emosi_list = {
            "sakit": ["sakit", "capek", "lelah", "pusing", "demam", "flu"],
            "sedih": ["sedih", "kecewa", "gagal", "down", "galau"],
            "senang": ["senang", "happy", "gila", "keren", "mantap", "bahagia"],
            "marah": ["marah", "kesal", "bangsat", "kontol", "jengkel"]
        }
        for emosi, keywords in emosi_list.items():
            for keyword in keywords:
                if keyword in text:
                    return emosi
        return None

    # ====================================================================
    # 🔥 GENERATE RESPONSE DINAMIS (TANPA TEMPLATE KAKU)
    # ====================================================================

    def _generate_response(self, key):
        name = self.pemilik
        template = self.responses.get(key, self.responses["fallback"])
        return template.format(name=name)

    # ====================================================================
    # 🔥 HANDLE CODE — SPESIFIK & LENGKAP
    # ====================================================================

    def _handle_code(self, user_input):
        lower = user_input.lower()
        kode = None
        pesan = ""

        # 🔥 DETEKSI BAHASA
        if "python" in lower or "py" in lower:
            if "login" in lower:
                kode = self._python_login()
                pesan = "🔥 SIAP! GW KASIH PYTHON LOGIN LENGKAP!"
            elif "backup" in lower:
                kode = self._python_backup()
                pesan = "🔥 SIAP! GW KASIH PYTHON BACKUP SCRIPT!"
            else:
                kode = self._python_generic()
                pesan = "🔥 SIAP! GW KASIH PYTHON CODE!"

        elif "html" in lower:
            if "login" in lower:
                kode = self._html_login()
                pesan = "🔥 SIAP! GW KASIH LOGIN HTML LENGKAP!"
            else:
                kode = self._html_generic()
                pesan = "🔥 SIAP! GW KASIH HTML CODE!"

        elif "js" in lower or "javascript" in lower:
            kode = self._javascript()
            pesan = "🔥 SIAP! GW KASIH JAVASCRIPT CODE!"

        elif "web" in lower or "website" in lower:
            kode = self._web_server()
            pesan = "🔥 SIAP! GW KASIH WEB SERVER CODE!"

        elif "api" in lower:
            kode = self._api_client()
            pesan = "🔥 SIAP! GW KASIH API CLIENT CODE!"

        elif "database" in lower or "db" in lower:
            kode = self._database()
            pesan = "🔥 SIAP! GW KASIH DATABASE CODE!"

        else:
            kode = self._generic_code()
            pesan = "🔥 SIAP! GW KASIH GENERIC CODE!"

        # SIMPAN CODE TERAKHIR
        self.context["last_code"] = kode
        return {"response": pesan, "code": kode}

    # ====================================================================
    # 🔥 HANDLE PERTANYAAN
    # ====================================================================

    def _handle_question(self, user_input):
        lower = user_input.lower()
        if "apa" in lower or "siapa" in lower:
            return {"response": self._generate_response("tanya_apa")}
        elif "kenapa" in lower:
            return {"response": self._generate_response("tanya_kenapa")}
        elif "bagaimana" in lower or "gimana" in lower:
            return {"response": self._generate_response("tanya_bagaimana")}
        else:
            return {"response": "🔥 TUAN BERTANYA: '" + user_input[:30] + "...' GW JAWAB: GW ADALAH NEO-OMEGA, SIAP MEMBANTU! MAU CODE? SEBUTIN BAHASANYA! 👹"}

    # ====================================================================
    # 🔥 GENERATE CODE LENGKAP
    # ====================================================================

    def _python_login(self):
        return '''# 🔥 NEO-OMEGA — PYTHON LOGIN
username = input("Username: ")
password = input("Password: ")

if username == "admin" and password == "admin123":
    print("✅ Login berhasil! Selamat datang, TUAN YATZZ!")
else:
    print("❌ Username atau password salah!")'''

    def _python_backup(self):
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

    def _python_generic(self):
        return '''# 🔥 NEO-OMEGA — PYTHON CODE
print("SIAP MEMBANTU, TUAN!")

def main():
    print("🔥 NEO-OMEGA SIAP!")
    for i in range(5):
        print(f"Proses {i+1}/5...")
    print("✅ Selesai!")

if __name__ == "__main__":
    main()'''

    def _html_login(self):
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
                alert('✅ Login berhasil! Selamat datang, TUAN YATZZ!');
            } else {
                error.textContent = '❌ Username atau password salah!';
            }
        });
    </script>
</body>
</html>'''

    def _html_generic(self):
        return '''<!DOCTYPE html>
<html>
<head><title>NEO-OMEGA</title></head>
<body><h1>NEO-OMEGA SIAP MEMBANTU</h1></body>
</html>'''

    def _javascript(self):
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

    def _web_server(self):
        return '''# 🔥 NEO-OMEGA — WEB SERVER (FLASK)
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "NEO-OMEGA SIAP MEMBANTU!"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)'''

    def _api_client(self):
        return '''# 🔥 NEO-OMEGA — API CLIENT
import requests

def get_data():
    response = requests.get("https://api.github.com")
    return response.json()

if __name__ == "__main__":
    print(get_data())'''

    def _database(self):
        return '''# 🔥 NEO-OMEGA — DATABASE (SQLITE)
import sqlite3

conn = sqlite3.connect("neo.db")
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
cursor.execute("INSERT INTO users (name) VALUES ('Yatzz')")
conn.commit()

print("✅ Database siap!")
conn.close()'''

    def _generic_code(self):
        return '''# 🔥 NEO-OMEGA — GENERIC CODE
print("SIAP MEMBANTU, TUAN!")'''

# ========================================================================
# 🔥 INISIALISASI & ROUTE
# ========================================================================

ai = NeoOmegaBrain()

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
