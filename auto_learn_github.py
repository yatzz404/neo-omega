import os
import json
import time
import random
import requests
import subprocess
import sys
from bs4 import BeautifulSoup

class AutoLearnAI:
    def __init__(self):
        self.memory_file = "auto_memory.json"
        self.learned_codes = []
        self.patterns = {}
        self.success_count = 0
        self.error_count = 0
        self._load_memory()
        print("[+] NEO OMEGA AI - AUTO-LEARN (GITHUB ACTIONS)")
        print("[+] CREATED BY YATZZ")
    
    def _load_memory(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file, "r") as f:
                data = json.load(f)
                self.learned_codes = data.get("learned_codes", [])
                self.patterns = data.get("patterns", {})
                self.success_count = data.get("success_count", 0)
                self.error_count = data.get("error_count", 0)
        else:
            self.learned_codes = []
            self.patterns = {}
            self.success_count = 0
            self.error_count = 0
    
    def _save_memory(self):
        with open(self.memory_file, "w") as f:
            json.dump({
                "learned_codes": self.learned_codes,
                "patterns": self.patterns,
                "success_count": self.success_count,
                "error_count": self.error_count
            }, f, indent=2)
        print("[+] Memory saved!")
    
    def generate_code(self, intent="web_server"):
        patterns = {
            "web_server": '''
from flask import Flask
app = Flask(__name__)
@app.route('/')
def home():
    return "Hello, World!"
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
''',
            "scraper": '''
import requests
from bs4 import BeautifulSoup
url = "https://example.com"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
print(soup.title.text)
''',
            "ai": '''
import numpy as np
class NeuralNetwork:
    def __init__(self):
        self.weights = np.random.randn(10, 10)
    def predict(self, x):
        return np.dot(x, self.weights)
nn = NeuralNetwork()
print(nn.predict(np.array([1,2,3,4,5,6,7,8,9,10])))
'''
        }
        return patterns.get(intent, "print('NEO OMEGA AI - AUTO-GENERATED')")
    
    def test_code(self, code):
        with open("temp_test.py", "w") as f:
            f.write(code)
        try:
            result = subprocess.run(["python3", "temp_test.py"], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                self.success_count += 1
                return True, result.stdout
            else:
                self.error_count += 1
                return False, result.stderr
        except:
            self.error_count += 1
            return False, "Error"
    
    def learn(self, iterations=3):
        intents = ["web_server", "scraper", "ai"]
        for i in range(iterations):
            intent = random.choice(intents)
            code = self.generate_code(intent)
            success, output = self.test_code(code)
            if success:
                self.learned_codes.append({"intent": intent, "code": code, "success": True})
                self.patterns[intent] = self.patterns.get(intent, 0) + 1
                print(f"[+] {intent} - SUCCESS")
            else:
                print(f"[-] {intent} - FAILED")
            self._save_memory()
        print(f"[+] Learned {len(self.learned_codes)} codes")

if __name__ == "__main__":
    ai = AutoLearnAI()
    ai.learn(iterations=3)
