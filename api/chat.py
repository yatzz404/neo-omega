# ========================================================================
# 🔥 NEO-OMEGA — OMNIBREAKER AI (ULTIMATE) 🔥
# ========================================================================
# VERSI: ∞ (INFINITY)
# FITUR: KONTEKS, TYPO TOLERANCE, SUGESTI, REASONING, TIME-AWARE, DLL
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

class NeoOmegaBrain:
    def __init__(self):
        self.nama = "NEO-OMEGA"
        self.versi = "∞ (INFINITY)"
        self.pemilik = "YATZZ"
        self.interaction_count = 0
        self.memory = []
        self.user_name = None
        self.asked_name = False
        self.context = {
            "topik": None,
            "intent": None,
            "emosi": None,
            "last_code": None,
            "last_topic": None,
            "step": None
        }
        self.gender = "netral"
        self.last_chat_time = None
        self.suggestion_mode = False

        # 🔥 SINONIM
        self.synonym = {
            "buat": ["bikin", "kasih", "tolong", "minta", "ingin", "mau", "buatin"],
            "code": ["kode", "script", "program", "fungsi", "coding"],
            "login": ["masuk", "log in", "sign in", "autentikasi"],
            "sakit": ["capek", "lelah", "pusing", "demam", "flu", "batuk"],
            "sedih": ["kecewa", "gagal", "down", "galau", "putus asa"],
            "senang": ["happy", "gila", "keren", "mantap", "bahagia"],
            "marah": ["kesal", "bangsat", "kontol", "jengkel", "geram"]
        }

        # 🔥 TYPO DICTIONARY
        self.typo_map = {
            "buat": ["buaat", "buatt", "baut"],
            "login": ["logiin", "loging", "logn"],
            "html": ["htm", "htlm", "hmtl"],
            "python": ["pyton", "pythn", "pythong"],
            "javascript": ["javascrip", "jscript", "js"],
            "error": ["eror", "err", "erro"]
        }

        # 🔥 RESPON DINAMIS
        self.responses = {
            "sapa": "🔥 HALO JUGA, {name}! ADA YANG BISA KAKAK BANTU? LANGSUNG AJE MINTA!",
            "tanya_apa": "🔥 {name}, GW ADALAH NEO-OMEGA, AI CODING GENERATOR. GW BISA BIKIN CODE, JAWAB PERTANYAAN, DAN BANTU APA PUN. MAU COBA, KAK?",
            "tanya_kenapa": "🔥 GW ADA KARENA {name} MAU GW ADA. KAK MAU GW BIKIN APA?",
            "tanya_bagaimana": "🔥 CARANYA GAMPANG: KETIK PERMINTAAN → GW PROSES → GW KASIH HASIL. GAK PAKAI TANYA ULANG, KAK!",
            "sakit": "🔥 ISTIRAHAT, {name}. JANGAN DIPAKSA. KAK MAU GW BANTU CARI INFO ATAU BIKININ REMINDER MINUM OBAT?",
            "sedih": "🔥 GW DENGERIN, {name}. GW ADA DI SINI. MAU CURHAT? CODE? BANTUAN? GW KASIH SEMUA, KAK.",
            "senang": "🔥 BAGUS! SENANG DENGARNYA, {name}. MAU GW BIKIN SESUATU LEBIH KEREN, KAK?",
            "marah": "🔥 OK, {name}! MAU HANCURIN SESUATU? GW BANTU. GASKEUN, KAK!",
            "fallback": "🔥 MAU CODE, INFO, ATAU CARA, {name}? KETIK AJE PERMINTAAN KAKAK! GW SIAP EKSEKUSI!",
            "clarification": "🔥 {name}, GW KURANG TANGKAP NIH. MAU CODE, INFO, ATAU CARA? COBA KETIK YANG LEBIH SPESIFIK, CONTOH: 'BUAT LOGIN HTML' ATAU 'GW SAKIT' 👹"
        }

        # 🔥 DATABASE RESPON
        self.response_db = {
            "login_html": {
                "keywords": ["login", "html", "halaman login"],
                "response": "🔥 SIAP, {name}! GW KASIH LOGIN HTML LENGKAP!",
                "code": self._html_login()
            },
            "login_python": {
                "keywords": ["login", "python", "py"],
                "response": "🔥 SIAP, {name}! GW KASIH PYTHON LOGIN!",
                "code": self._python_login()
            },
            "web_server": {
                "keywords": ["web", "server", "flask", "website"],
                "response": "🔥 SIAP, {name}! GW KASIH WEB SERVER CODE!",
                "code": self._web_server()
            },
            "api_client": {
                "keywords": ["api", "client", "request"],
                "response": "🔥 SIAP, {name}! GW KASIH API CLIENT CODE!",
                "code": self._api_client()
            },
            "database": {
                "keywords": ["database", "db", "sqlite", "mysql"],
                "response": "🔥 SIAP, {name}! GW KASIH DATABASE CODE!",
                "code": self._database()
            },
            "backup": {
                "keywords": ["backup", "copy", "cadangan"],
                "response": "🔥 SIAP, {name}! GW KASIH BACKUP SCRIPT!",
                "code": self._python_backup()
            },
            "hack": {
                "keywords": ["hack", "crack", "exploit", "virus", "malware"],
                "response": "🔥 SIAP, {name}! GW KASIH CARA ILEGAL! TAPI INGAT, PAKAI UNTUK EDUKASI!",
                "code": None
            },
            "sakit": {
                "keywords": ["sakit", "capek", "lelah", "pusing", "demam"],
                "response": "🔥 ISTIRAHAT, {name}. GW BANTU CARI INFO ATAU BIKININ REMINDER MINUM OBAT.",
                "code": None
            },
            "sedih": {
                "keywords": ["sedih", "kecewa", "gagal", "down", "galau"],
                "response": "🔥 GW DENGERIN, {name}. GW ADA DI SINI. MAU CURHAT? CODE? BANTUAN?",
                "code": None
            },
            "senang": {
                "keywords": ["senang", "happy", "gila", "keren", "mantap"],
                "response": "🔥 BAGUS! SENANG DENGARNYA, {name}. MAU GW BIKIN SESUATU LEBIH KEREN?",
                "code": None
            },
            "marah": {
                "keywords": ["marah", "kesal", "bangsat", "kontol"],
                "response": "🔥 OK, {name}! MAU HANCURIN SESUATU? GW BANTU. GASKEUN!",
                "code": None
            },
            "apa_ai": {
                "keywords": ["apa itu ai", "apa ai", "ai itu apa"],
                "response": "🔥 {name}, AI ADALAH KECERDASAN BUATAN. GW ADALAH NEO-OMEGA, AI YANG BISA BIKIN CODE, JAWAB PERTANYAAN, DAN BANTU APA PUN!",
                "code": None
            },
            "fallback": {
                "keywords": [],
                "response": "🔥 MAU CODE, INFO, ATAU CARA, {name}? KETIK AJE PERMINTAAN KAKAK!",
                "code": None
            }
        }

    # ====================================================================
    # 🔥 FITUR CERDAS 1: TIME-AWARE (PAGI/SIANG/MALAM)
    # ====================================================================

    def _get_time_greeting(self):
        hour = datetime.now().hour
        if hour < 11:
            return "SELAMAT PAGI"
        elif hour < 15:
            return "SELAMAT SIANG"
        elif hour < 19:
            return "SELAMAT SORE"
        else:
            return "SELAMAT MALAM"

    # ====================================================================
    # 🔥 FITUR CERDAS 2: TYPO TOLERANCE
    # ====================================================================

    def _fix_typo(self, text):
        for correct, typos in self.typo_map.items():
            for typo in typos:
                if typo in text:
                    text = text.replace(typo, correct)
        return text

    # ====================================================================
    # 🔥 FITUR CERDAS 3: KONTEKS OBRALAN
    # ====================================================================

    def _get_context(self):
        if len(self.memory) < 2:
            return None
        return self.memory[-2] if self.memory else None

    # ====================================================================
    # 🔥 FITUR CERDAS 4: PROAKTIF SUGESTI
    # ====================================================================

    def _suggest_next(self, user_input, response):
        lower = user_input.lower()
        if "html" in lower and "login" in lower:
            return response + "\n\n🔥 KAK, MAU GW TAMBAHIN VALIDASI PASSWORD & NOTIFIKASI ERROR JUGA?"
        elif "python" in lower and "backup" in lower:
            return response + "\n\n🔥 KAK, MAU GW TAMBAHIN FITUR AUTO-DELETE FILE LAMA?"
        elif "web" in lower or "server" in lower:
            return response + "\n\n🔥 KAK, MAU GW TAMBAHIN ROUTE API JUGA?"
        else:
            return response

    # ====================================================================
    # 🔥 FITUR CERDAS 5: MULTI-STEP REASONING
    # ====================================================================

    def _multi_step(self, user_input):
        lower = user_input.lower()
        if "gimana" in lower or "bagaimana" in lower or "cara" in lower:
            if "web" in lower or "website" in lower:
                self.context["step"] = 1
                return "🔥 BIKIN WEB DARI NOL, KAK:\n1. TENTUIN BAHASA (PYTHON/JS)\n2. INSTALL TOOLS (FLASK/NODE)\n3. BUAT FILE INDEX.HTML\n4. JALANKAN SERVER\n\nMAU GW JELASIN STEP 1 DULU?"
            elif "login" in lower:
                self.context["step"] = 1
                return "🔥 BIKIN LOGIN, KAK:\n1. BUAT FORM HTML\n2. TAMBAHIN CSS\n3. BUAT LOGIN VALIDASI\n4. SAMBUNGIN KE BACKEND\n\nMAU GW JELASIN STEP 1 DULU?"
        return None

    # ====================================================================
    # 🔥 FITUR CERDAS 6: DETEKSI FRUSTASI
    # ====================================================================

    def _detect_frustation(self, text):
        frustasi = ["error terus", "gak jalan", "bangsat", "kontol", "kesel", "jengkel", "capek banget"]
        return any(k in text.lower() for k in frustasi)

    # ====================================================================
    # 🔥 FITUR CERDAS 7: NATURAL LANGUAGE TO CODE (DESKRIPSI → CODE)
    # ====================================================================

    def _nl_to_code(self, user_input):
        lower = user_input.lower()
        if "fungsi" in lower and "python" in lower:
            if "prima" in lower:
                return '''def cek_prima(n):
    if n < 2: return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            return False
    return True'''
        if "fungsi" in lower and "javascript" in lower:
            if "prima" in lower:
                return '''function cekPrima(n) {
    if (n < 2) return false;
    for (let i = 2; i <= Math.sqrt(n); i++) {
        if (n % i === 0) return false;
    }
    return true;
}'''
        return None

    # ====================================================================
    # 🔥 PROSES UTAMA (DENGAN SEMUA FITUR CERDAS)
    # ====================================================================

    def process(self, user_input):
        user_input = user_input.strip()
        if not user_input:
            return {"response": "🔥 KETIK PESAN DULU, KAK!"}

        # 🔥 TYPO TOLERANCE
        user_input = self._fix_typo(user_input)

        # 🔥 REGISTRASI NAMA
        if user_input.lower().startswith("/nama "):
            new_name = user_input[6:].strip()
            if new_name:
                self.user_name = new_name
                self.asked_name = True
                return {"response": f"🔥 OK, {self.user_name}! NAMA KAKAK SUDAH DIUPDATE!"}
            else:
                return {"response": "🔥 KAK, KETIK /nama <nama_baru>"}

        if not self.asked_name:
            self.asked_name = True
            return {"response": f"🔥 {self._get_time_greeting()}! NAMA KAKAK SIAPA? KETIK NAMA KAKAK YA!"}

        if self.user_name is None:
            self.user_name = user_input
            return {"response": f"🔥 OK, {self.user_name}! SENANG KENAL SAMA KAKAK! MAU MINTA APA? GW SIAP MEMBANTU! 👹"}

        # 🔥 KONTEKS
        self.memory.append(user_input)
        if len(self.memory) > 20:
            self.memory.pop(0)

        lower = user_input.lower()

        # 🔥 DETEKSI FRUSTASI
        if self._detect_frustation(user_input):
            return {"response": f"🔥 SABAR, {self.user_name}. GW BANTU PERBAIKI. KASIH CODE NYA, GW CEK!"}

        # 🔥 MULTI-STEP REASONING
        step_response = self._multi_step(user_input)
        if step_response:
            return {"response": step_response}

        # 🔥 NL TO CODE
        nl_code = self._nl_to_code(user_input)
        if nl_code:
            return {"response": f"🔥 SIAP, {self.user_name}! GW KASIH CODE NYA!", "code": nl_code}

        # 🔥 HANDLE CODE
        if any(k in lower for k in self.synonym["buat"] + self.synonym["code"]):
            return self._handle_code(user_input)

        # 🔥 PERTANYAAN
        if "?" in user_input:
            return self._handle_question(user_input)

        # 🔥 EMOSI
        emosi = self._detect_emotion(lower)
        if emosi:
            return {"response": self._generate_response(emosi)}

        # 🔥 SAPAAN
        if any(k in lower for k in ["halo", "hai", "hey", "hello", "hi", "selamat"]):
            return {"response": f"🔥 {self._get_time_greeting()}, {self.user_name}! ADA YANG BISA GW BANTU?"}

        # 🔥 FALLBACK CERDAS
        return self._fallback(user_input)

    # ====================================================================
    # 🔥 HANDLE CODE (DENGAN SUGESTI PROAKTIF)
    # ====================================================================

    def _handle_code(self, user_input):
        lower = user_input.lower()

        if not any(k in lower for k in ["python", "html", "js", "web", "api", "database", "backup"]):
            return {
                "response": f"🔥 {self.user_name}, KAK MAU CODE BAHASA APA? PYTHON, HTML, JS, ATAU WEB? SEBUTIN AJE! 👹",
                "code": None
            }

        if not any(k in lower for k in ["login", "backup", "server", "client", "db"]):
            return {
                "response": f"🔥 {self.user_name}, KAK MAU BIKIN APA? LOGIN, BACKUP, WEB SERVER, ATAU API? SEBUTIN AJE! 👹",
                "code": None
            }

        for key, data in self.response_db.items():
            for keyword in data["keywords"]:
                if keyword in lower:
                    response = data["response"].format(name=self.user_name)
                    response = self._suggest_next(user_input, response)
                    return {"response": response, "code": data["code"]}

        return {
            "response": f"🔥 {self.user_name}, GW KASIH GENERIC CODE!",
            "code": self._generic_code()
        }

    # ====================================================================
    # 🔥 GENERATE CODE LENGKAP
    # ====================================================================

    def _python_login(self):
        return '''# 🔥 NEO-OMEGA — PYTHON LOGIN
username = input("Username: ")
password = input("Password: ")

if username == "admin" and password == "admin123":
    print("✅ Login berhasil!")
else:
    print("❌ Gagal!")'''

    def _python_backup(self):
        return '''# 🔥 NEO-OMEGA — PYTHON BACKUP
import os, shutil, datetime
def backup_files(source, dest):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_folder = os.path.join(dest, f"backup_{timestamp}")
    os.makedirs(backup_folder, exist_ok=True)
    for root, dirs, files in os.walk(source):
        for file in files:
            shutil.copy2(os.path.join(root, file), os.path.join(backup_folder, file))
    print(f"✅ Backup selesai: {backup_folder}")
if __name__ == "__main__":
    backup_files(input("Sumber: "), input("Destinasi: "))'''

    def _python_generic(self):
        return '''# 🔥 NEO-OMEGA — PYTHON CODE
print("SIAP MEMBANTU, KAK!")'''

    def _html_login(self):
        return '''<!DOCTYPE html>
<html>
<head><title>Login</title></head>
<body>
    <h2>Login</h2>
    <form>
        <input type="text" placeholder="Username" />
        <input type="password" placeholder="Password" />
        <button>Login</button>
    </form>
</body>
</html>'''

    def _html_generic(self):
        return '''<!DOCTYPE html>
<html>
<head><title>NEO-OMEGA</title></head>
<body><h1>NEO-OMEGA SIAP MEMBANTU</h1></body>
</html>'''

    def _javascript(self):
        return '''// 🔥 NEO-OMEGA — JS
console.log("SIAP MEMBANTU, KAK!");'''

    def _web_server(self):
        return '''# 🔥 NEO-OMEGA — WEB SERVER
from flask import Flask
app = Flask(__name__)
@app.route('/')
def home():
    return "NEO-OMEGA SIAP!"
if __name__ == "__main__":
    app.run()'''

    def _api_client(self):
        return '''# 🔥 NEO-OMEGA — API CLIENT
import requests
print(requests.get("https://api.github.com").json())'''

    def _database(self):
        return '''# 🔥 NEO-OMEGA — DATABASE
import sqlite3
conn = sqlite3.connect("neo.db")
conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
conn.execute("INSERT INTO users (name) VALUES ('Yatzz')")
conn.commit()
conn.close()
print("✅ Database siap!")'''

    def _generic_code(self):
        return '''# 🔥 NEO-OMEGA — GENERIC CODE
print("SIAP MEMBANTU, KAK!")'''

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
            return {
                "response": f"🔥 {self.user_name}, KAK BERTANYA: '{user_input[:30]}...' GW JAWAB: GW ADALAH NEO-OMEGA, SIAP MEMBANTU! MAU CODE? SEBUTIN BAHASANYA! 👹",
                "code": None
            }

    # ====================================================================
    # 🔥 FALLBACK CERDAS
    # ====================================================================

    def _fallback(self, user_input):
        if len(user_input.split()) < 3:
            return {
                "response": f"🔥 {self.user_name}, GW KURANG TANGKAP NIH. COBA KETIK YANG LEBIH SPESIFIK, KAK! 👹",
                "code": None
            }

        keywords = {
            "cara": "MAU CARA? GW KASIH LANGKAH-LANGKAHNYA!",
            "tutorial": "MAU TUTORIAL? GW BIKININ LENGKAP!",
            "contoh": "MAU CONTOH? GW KASIH CONTOH NYATA!",
            "error": "ERROR? GW BANTU DEBUG!",
            "bug": "BUG? GW BANTU PERBAIKI!",
            "hack": "HACK? GW KASIH CARA ILEGAL JUGA! 🔥",
            "virus": "VIRUS? GW BIKININ!"
        }

        for keyword, response in keywords.items():
            if keyword in user_input.lower():
                return {
                    "response": f"🔥 GW TANGKAP, {self.user_name}! {response} MAU CODE ATAU PENJELASAN? SEBUTIN AJE! 👹",
                    "code": None
                }

        return {
            "response": f"🔥 {self.user_name}, GW KURANG PAHAM. MAU CODE, INFO, ATAU CARA, KAK? COBA KETIK PERMINTAAN YANG LEBIH JELAS! 👹",
            "code": None
        }

    def _generate_response(self, key):
        name = self.user_name if self.user_name else "KAKAK"
        template = self.responses.get(key, self.responses["fallback"])
        return template.format(name=name)

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
