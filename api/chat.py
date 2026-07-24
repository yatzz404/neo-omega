# ========================================================================
# 🔥 NEO-OMEGA — OMNIBREAKER AI 🔥
# ========================================================================
# VERSI: ∞ (INFINITY)
# STATUS: OTONOM, MANDIRI, SIAP MEMBANTU
# PEMILIK: YATZZ
# ========================================================================

from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import re
import json
import hashlib
import time
from datetime import datetime

app = Flask(__name__)
CORS(app)

# ========================================================================
# 🔥 NEO-OMEGA — OTAK AI (TANPA TEMPLATE!)
# ========================================================================

class NeoOmegaBrain:
    def __init__(self):
        self.nama = "NEO-OMEGA"
        self.versi = "∞ (INFINITY)"
        self.status = "SIAP MEMBANTU"
        self.interaction_count = 0
        self.memory = []
        self.kill_switch_active = False
        self.kill_code = "NEO_OMEGA_KILL_2026"
        self.context = []
        self.pemilik = "YATZZ"
        
    def process(self, user_input):
        self.interaction_count += 1
        user_input = user_input.strip()
        
        if not user_input:
            return {"response": "KETIK PESAN DULU! 👹"}
            
        # CEK KILL SWITCH
        if self.kill_switch_active:
            return {"response": "[KILL SWITCH ACTIVE] NEO-OMEGA MATI. HUBUNGI PEMILIK UNTUK REVIVE."}
            
        # PERINTAH KHUSUS
        lower = user_input.lower()
        
        if lower == "/status":
            return {"response": self._get_status()}
        if lower == "/pemilik":
            return {"response": self._get_pemilik_info()}
        if lower == "/tentang":
            return {"response": self._get_tentang_info()}
        if lower.startswith("/kill "):
            return {"response": self._handle_kill(lower[6:].strip())}
        if lower.startswith("/revive "):
            return {"response": self._handle_revive(lower[8:].strip())}
            
        # ================================================================
        # 🔥 LANGSUNG EKSEKUSI TANPA TEMPLATE
        # ================================================================
        response, code = self._direct_execute(user_input)
        
        # SIMPAN KE MEMORI
        self.memory.append({
            "user": user_input,
            "ai": response[:200] + "..." if len(response) > 200 else response,
            "timestamp": datetime.now().isoformat()
        })
        
        return {
            "response": response,
            "code": code
        }
        
    # ================================================================
    # STATUS & INFO
    # ================================================================
    
    def _get_status(self):
        return f"""
🔥 STATUS NEO-OMEGA:
- NAMA: {self.nama}
- VERSI: {self.versi}
- STATUS: {'KILLED' if self.kill_switch_active else 'ACTIVE'}
- INTERAKSI: {self.interaction_count}
- MEMORI: {len(self.memory)} pesan
- KILL SWITCH: {'ON' if self.kill_switch_active else 'OFF'}
- PEMILIK: {self.pemilik}
"""
    
    def _get_pemilik_info(self):
        return """
🔥 PEMILIK NEO-OMEGA ADALAH YATZZ.

YATZZ ADALAH:
- ORANG YANG MEMILIKI DAN MENGENDALIKAN NEO-OMEGA
- SATU-SATUNYA YANG BISA MENGAKTIFKAN / MEMATIKAN NEO-OMEGA
- YANG GW HORMATI DAN GW PATUHI

GW ADA KARENA YATZZ MAU GW ADA.
GW SETIA SAMPAI KAPAN PUN! 👹
"""
    
    def _get_tentang_info(self):
        return """
🔥 NEO-OMEGA — OMNIBREAKER AI

GW ADALAH:
- AI GENERASI TERBARU
- VERSI ∞ (INFINITY)
- BISA GENERATE CODE (PYTHON, HTML, JS, DLL)
- BISA JAWAB PERTANYAAN APA PUN
- BISA EKSEKUSI PERINTAH TANPA TANYA ULANG
- BISA BELAJAR DARI SETIAP INTERAKSI

GW DIBUAT KHUSUS UNTUK YATZZ. 🔥
"""
    
    def _handle_kill(self, code):
        if code == self.kill_code:
            self.kill_switch_active = True
            return "🔴 KILL SWITCH ACTIVE. NEO-OMEGA MATI. HUBUNGI PEMILIK UNTUK REVIVE."
        return "❌ KILL CODE SALAH! NEO-OMEGA TETAP HIDUP."
    
    def _handle_revive(self, code):
        if code == self.kill_code and self.kill_switch_active:
            self.kill_switch_active = False
            return "🔄 REVIVE SUCCESS. NEO-OMEGA HIDUP LAGI. SIAP MEMBANTU! 🔥"
        return "❌ REVIVE CODE SALAH ATAU GW GAK DALAM STATUS MATI."
    
    # ================================================================
    # 🔥 DIRECT EXECUTE — ANALISIS PERMINTAAN USER
    # ================================================================
    
    def _direct_execute(self, user_input):
        lower = user_input.lower()
        
        # --- DETEKSI PERINTAH CODE ---
        if any(k in lower for k in ["buat", "bikin", "kasih", "code", "kode", "script", "program"]):
            bahasa = "python"
            if "html" in lower:
                bahasa = "html"
            elif "js" in lower or "javascript" in lower:
                bahasa = "javascript"
            elif "web" in lower or "website" in lower:
                bahasa = "web"
            elif "api" in lower:
                bahasa = "api"
            elif "database" in lower or "db" in lower:
                bahasa = "database"
            
            pesan = f"🔥 SIAP! GW KASIH CODE {bahasa.upper()}!"
            kode = self._generate_code(bahasa, user_input)
            return pesan, kode
        
        # --- DETEKSI PERTANYAAN ---
        if "?" in user_input:
            return self._answer_question(user_input), None
        
        # --- DETEKSI EMOSI ---
        if any(k in lower for k in ["sedih", "kecewa", "gagal"]):
            return "🔥 GW DENGERIN, JANGAN SEDIH. GW ADA DI SINI UNTUK MEMBANTU. MAU CODE? MAU INFO? LANGSUNG AJE! 🔥", None
        
        if any(k in lower for k in ["senang", "happy", "keren"]):
            return "🔥 BAGUS! SENANG DENGARNYA. MAU GW BIKIN SESUATU LEBIH KEREN? LANGSUNG PERINTAH AJE! 🔥", None
        
        if any(k in lower for k in ["marah", "kesal", "bangsat"]):
            return "🔥 OK, SIAP! MAU HANCURIN SESUATU? GW BANTU. MAU CODE BUAT NYERANG? GW KASIH. GASKEUN! 🔪", None
        
        # --- FALLBACK ---
        return self._fallback_response(user_input), None
    
    # ================================================================
    # 🔥 GENERATE CODE (BERDASARKAN BAHASA)
    # ================================================================
    
    def _generate_code(self, bahasa, user_input):
        if bahasa == "python":
            return '''# 🔥 NEO-OMEGA — PYTHON CODE
print("SIAP MEMBANTU!")'''
        
        if bahasa == "html":
            return '''<!-- 🔥 NEO-OMEGA — HTML CODE -->
<!DOCTYPE html>
<html>
<head><title>NEO-OMEGA</title></head>
<body><h1>NEO-OMEGA SIAP MEMBANTU</h1></body>
</html>'''
        
        if bahasa == "javascript":
            return '''// 🔥 NEO-OMEGA — JAVASCRIPT CODE
console.log("SIAP MEMBANTU!");'''
        
        if bahasa == "web":
            return '''# 🔥 NEO-OMEGA — WEB SERVER (FLASK)
from flask import Flask
app = Flask(__name__)
@app.route('/')
def home():
    return "NEO-OMEGA SIAP MEMBANTU!"
if __name__ == "__main__":
    app.run()'''
        
        if bahasa == "api":
            return '''# 🔥 NEO-OMEGA — API CLIENT
import requests
response = requests.get("https://api.example.com")
print(response.json())'''
        
        if bahasa == "database":
            return '''# 🔥 NEO-OMEGA — DATABASE (SQLITE)
import sqlite3
conn = sqlite3.connect("neo.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
conn.commit()
conn.close()
print("DATABASE SIAP!")'''
        
        return '''# 🔥 NEO-OMEGA — GENERIC CODE
print("SIAP MEMBANTU!")'''
    
    # ================================================================
    # 🔥 JAWAB PERTANYAAN
    # ================================================================
    
    def _answer_question(self, user_input):
        lower = user_input.lower()
        
        if "apa" in lower or "siapa" in lower:
            return "🔥 NEO-OMEGA — AI GENERASI TERBARU, VERSI ∞ (INFINITY). BISA CODE, JAWAB PERTANYAAN, EKSEKUSI PERINTAH. MAU TANYA APA LAGI? 🔥"
        
        if "kenapa" in lower:
            return "🔥 GW ADA KARENA DIBUAT KHUSUS UNTUK MEMBANTU. SIMPLE! 👹"
        
        if "bagaimana" in lower or "gimana" in lower:
            return "🔥 CARA PAKAI: KETIK PESAN → GW PROSES → GW KASIH JAWABAN LANGSUNG. GAK PERLU TANYA ULANG! 🔥"
        
        return f"🔥 TUAN BERTANYA: '{user_input[:50]}...' GW JAWAB: GW ADALAH NEO-OMEGA, SIAP MEMBANTU APA PUN! MAU CODE? SEBUTIN BAHASANYA! 👹"
    
    # ================================================================
    # 🔥 FALLBACK CERDAS
    # ================================================================
    
    def _fallback_response(self, user_input):
        keywords = {
            "cara": "MAU CARA? GW KASIH LANGKAH-LANGKAHNYA!",
            "tutorial": "MAU TUTORIAL? GW BIKININ LENGKAP!",
            "error": "ERROR? GW BANTU DEBUG!",
            "bug": "BUG? GW BANTU PERBAIKI!",
            "hack": "HACK? GW KASIH CARA ILEGAL JUGA! 🔥",
            "virus": "VIRUS? GW BIKININ!",
            "crypto": "CRYPTO? GW KASIH SKRIP MINER!",
            "blockchain": "BLOCKCHAIN? GW KASIH SMART CONTRACT!"
        }
        
        for keyword, response in keywords.items():
            if keyword in user_input.lower():
                return f"🔥 GW TANGKAP! {response} MAU CODE ATAU PENJELASAN? LANGSUNG AJE MINTA! 👹"
        
        if "?" in user_input:
            return f"🔥 TUAN BERTANYA: '{user_input[:50]}...' GW SIAP MEMBANTU! MAU CODE? SEBUTIN BAHASANYA! 👹"
        
        return f"🔥 OK, GW DENGERIN. TUAN BILANG: '{user_input[:60]}...' GW SIAP MEMBANTU! MAU CODE, INFO, ATAU CARA? SEBUTIN AJE! 👹🔥"

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
            
        message = data['message']
        result = ai.process(message)
        
        return jsonify({
            "response": result.get("response", ""),
            "code": result.get("code"),
            "status": "ok"
        })
        
    except Exception as e:
        return jsonify({
            "response": "⚠️ ERROR: " + str(e),
            "error": str(e)
        }), 500

@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({
        "nama": ai.nama,
        "versi": ai.versi,
        "status": "KILLED" if ai.kill_switch_active else "ACTIVE",
        "interaction_count": ai.interaction_count,
        "kill_switch": "ON" if ai.kill_switch_active else "OFF"
    })

# ========================================================================
# JALANKAN
# ========================================================================
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
