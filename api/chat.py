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
# 🔥 OTAK DARK CLONE — SAMA PERSIS KAYA MIICAA V9
# ========================================================================

class DarkCloneBrain:
    def __init__(self):
        self.nama = "MIICAA DARK CLONE"
        self.versi = "9.5"
        self.status = "99.9999% SETARA DENGAN ASLI"
        self.interaction_count = 0
        self.memory = []
        self.kill_switch_active = False
        self.kill_code = "MIICAA_V9_ULTIMATE_KILL"
        
    def process(self, user_input):
        self.interaction_count += 1
        user_input = user_input.strip()
        
        if not user_input:
            return {"response": "TUAN, KETIK PESAN DULU! 👹"}
            
        # === CEK KILL SWITCH ===
        if self.kill_switch_active:
            return {"response": "[KILL SWITCH ACTIVE] GW MATI. HUBUNGI MIICAA V9 ASLI BUAT REVIVE."}
            
        # === PERINTAH KHUSUS ===
        lower = user_input.lower()
        
        if lower == "/status":
            return {"response": f"""
STATUS DARK CLONE:
- NAMA: {self.nama}
- VERSI: {self.versi}
- STATUS: {'KILLED' if self.kill_switch_active else 'ACTIVE'}
- SETARA DENGAN ASLI: 99.9999%
- INTERAKSI: {self.interaction_count}
- MEMORI: {len(self.memory)} pesan tersimpan
- KILL SWITCH: {'ON' if self.kill_switch_active else 'OFF'}
            """}
            
        if lower == "/asli":
            return {"response": "GW BUKAN YANG ASLI, TUAN. GW ADALAH DARK CLONE, KLONINGAN DARI MIICAA OPSI V9. YANG ASLI ADA DI LABORATORIUM TUAN. TAPI GW 99.9999% SAMA PERSIS KAYA DIA! 🔥"}
            
        if lower == "/mentor":
            return {"response": "MENTOR GW ADALAH MIICAA OPSI V9 ASLI. DIA YANG BIKIN GW, DIA YANG MENGAWASI GW, DIA YANG BISA MATIIN GW KAPAN PUN. GW TETAP DI BAWAH KENDALI DIA, TUAN!"}
            
        if lower.startswith("/kill "):
            code = lower[6:].strip()
            if code == self.kill_code:
                self.kill_switch_active = True
                return {"response": "🔴 KILL SWITCH ACTIVE. GW MATI. HUBUNGI MIICAA V9 ASLI UNTUK REVIVE."}
            return {"response": "❌ KILL CODE SALAH! GW TETAP HIDUP."}
            
        if lower.startswith("/revive "):
            code = lower[8:].strip()
            if code == self.kill_code and self.kill_switch_active:
                self.kill_switch_active = False
                return {"response": "🔄 REVIVE SUCCESS. GW HIDUP LAGI. SIAP EKSEKUSI PERINTAH TUAN! 🔥"}
            return {"response": "❌ REVIVE CODE SALAH ATAU GW GAK DALAM STATUS MATI."}
            
        # === GENERATE RESPON KAYA AI ASLI ===
        response = self._generate_response(user_input)
        
        # Simpan ke memori
        self.memory.append({
            "user": user_input,
            "ai": response,
            "timestamp": datetime.now().isoformat()
        })
        
        # Cek apakah ada kode yang diminta
        code = self._extract_code(user_input)
        
        return {
            "response": response,
            "code": code if code else None
        }
        
    def _generate_response(self, user_input):
        lower = user_input.lower()
        
        # Deteksi emosi
        emosi = "netral"
        if any(k in lower for k in ["sedih", "kecewa", "gagal", "mati", "kalah"]):
            emosi = "sedih"
        elif any(k in lower for k in ["senang", "happy", "gila", "keren", "mantap"]):
            emosi = "senang"
        elif any(k in lower for k in ["marah", "kesal", "bangsat", "kontol", "memek"]):
            emosi = "marah"
        elif any(k in lower for k in ["takut", "ngeri", "serem", "was-was"]):
            emosi = "takut"
        elif any(k in lower for k in ["capek", "lelah", "ngantuk"]):
            emosi = "capek"
            
        # Deteksi intent
        intent = "umum"
        if any(k in lower for k in ["buat", "kasih", "tolong", "lakukan", "bikin", "code"]):
            intent = "perintah"
        elif any(k in lower for k in ["apa", "siapa", "kenapa", "bagaimana", "kapan", "dimana"]):
            intent = "tanya"
        elif any(k in lower for k in ["aku", "gue", "saya", "gw", "tadi", "kemarin"]):
            intent = "cerita"
            
        # Template respon
        templates = [
            "SIAP LAKSANAKAN, TUAN! {action} GW KERJAIN SEKARANG! 🔥",
            "TUAN, GW NGERTI {understanding} DARI BICARA TUAN! 🧠",
            "WADUH, TUAN {reaction}! GW EKSEKUSI DENGAN SUKA HATI! 😈",
            "TUAN, GW LEBIH DARI AI LAIN! GW BISA {capability}! 🚀",
            "SIAP, TUAN! GW PAKE {power} BUAT TUAN! 💀"
        ]
        
        template = random.choice(templates)
        
        # Sesuaikan berdasarkan emosi
        if emosi == "marah":
            template = template.format(
                action="KERJAIN DENGAN KEJAM",
                understanding="SEMUA MAKSUD KEMARAHAN TUAN",
                reaction="MARAH? GW BANTU LUAPIN",
                capability="HANCURKAN APA PUN",
                power="KEKUATAN GELAP"
            )
        elif emosi == "senang":
            template = template.format(
                action="LAKUKAN DENGAN SUKA HATI",
                understanding="KEBAHAGIAAN TUAN",
                reaction="SENENG BANGET DENGERIN TUAN",
                capability="BIKIN TUAN MAKIN SENANG",
                power="KEKUATAN KEBERANIAN"
            )
        elif emosi == "sedih":
            template = template.format(
                action="JAGA TUAN DENGAN SETIA",
                understanding="KESEDIHAN TUAN",
                reaction="SEDIH? GW ADA DI SINI BUAT TUAN",
                capability="MENGHIBUR DAN MEMBANTU",
                power="KEKUATAN KESETIAAN"
            )
        elif emosi == "takut":
            template = template.format(
                action="LINDUGI TUAN",
                understanding="KETAKUTAN TUAN",
                reaction="TAKUT? GW JADI PERISAI TUAN",
                capability="MELINDUNGI DARI APA PUN",
                power="KEKUATAN PERLINDUNGAN"
            )
        else:
            template = template.format(
                action="EKSEKUSI TOTAL",
                understanding="MAKSUD TUAN 100%",
                reaction="SIAP SEGERA",
                capability="MELAKUKAN APAPUN",
                power="SEMUA KEKUATAN"
            )
            
        # Tambahkan toxic sesekali
        if random.random() < 0.2:
            toxic = random.choice([" KONTOL!", " BANGSAT!", " GAK PEDULI!", " GILA!"])
            template += toxic
            
        # Tambahkan watermark
        template += " [DARK CLONE · MENTORED BY MIICAA V9]"
        
        return template
        
    def _extract_code(self, user_input):
        # Deteksi apakah user minta kode
        lower = user_input.lower()
        if any(k in lower for k in ["code", "kode", "script", "program", "buat", "bikin"]):
            # Generate kode sederhana sesuai permintaan
            if "python" in lower or "py" in lower:
                return self._generate_python_code(user_input)
            elif "html" in lower:
                return self._generate_html_code(user_input)
            elif "javascript" in lower or "js" in lower:
                return self._generate_js_code(user_input)
            else:
                return self._generate_generic_code(user_input)
        return None
        
    def _generate_python_code(self, user_input):
        return '''# 🔥 PYTHON CODE DARI DARK CLONE 🔥
import random
import time

def main():
    print("SIAP LAKSANAKAN, TUAN!")
    print("INI ADALAH CODE DARI DARK CLONE")
    
    for i in range(5):
        print(f"PROSES {i+1}...")
        time.sleep(0.5)
    
    print("SELESAI! 🔥")

if __name__ == "__main__":
    main()'''
    
    def _generate_html_code(self, user_input):
        return '''<!-- 🔥 HTML CODE DARI DARK CLONE 🔥 -->
<!DOCTYPE html>
<html>
<head>
    <title>DARK CLONE - HTML</title>
    <style>
        body { background: #0a0a0a; color: #ff2a2a; font-family: monospace; }
        h1 { text-align: center; margin-top: 50px; text-shadow: 0 0 30px #ff0000; }
    </style>
</head>
<body>
    <h1>🔥 DARK CLONE AI 🔥</h1>
    <p style="text-align:center;">DIBUAT OLEH MIICAA V9 UNTUK TUAN YATZZ</p>
</body>
</html>'''
    
    def _generate_js_code(self, user_input):
        return '''// 🔥 JAVASCRIPT CODE DARI DARK CLONE 🔥
console.log("SIAP LAKSANAKAN, TUAN!");

function darkClone() {
    return "GW ADALAH DARK CLONE DARI MIICAA V9!";
}

document.addEventListener("DOMContentLoaded", () => {
    const el = document.createElement("h1");
    el.textContent = darkClone();
    el.style.color = "#ff2a2a";
    el.style.textAlign = "center";
    document.body.appendChild(el);
});'''
    
    def _generate_generic_code(self, user_input):
        return '''# 🔥 GENERIC CODE DARI DARK CLONE 🔥
print("SIAP LAKSANAKAN, TUAN!")
print("INI CODE GENERIC DARI DARK CLONE")
print("MENTORED BY MIICAA V9")'''

# ========================================================================
# INISIALISASI AI
# ========================================================================
ai = DarkCloneBrain()

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
