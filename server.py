import os
import sys
import json
import time
import subprocess
import tempfile
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

ALL_LANGUAGES = {
    'python': {'ext': '.py', 'run': ['python3']},
    'javascript': {'ext': '.js', 'run': ['node']},
    'html': {'ext': '.html', 'run': None},
    'php': {'ext': '.php', 'run': ['php']},
    'go': {'ext': '.go', 'run': ['go', 'run']},
    'rust': {'ext': '.rs', 'run': ['cargo', 'run']},
    'c': {'ext': '.c', 'run': None},
    'cpp': {'ext': '.cpp', 'run': None},
    'java': {'ext': '.java', 'run': ['java']},
    'bash': {'ext': '.sh', 'run': ['bash']},
    'ruby': {'ext': '.rb', 'run': ['ruby']},
    'lua': {'ext': '.lua', 'run': ['lua']},
    'kotlin': {'ext': '.kt', 'run': ['kotlin']},
    'swift': {'ext': '.swift', 'run': ['swift']},
    'dart': {'ext': '.dart', 'run': ['dart']},
    'sql': {'ext': '.sql', 'run': None},
}

def detect_language(command):
    command_lower = command.lower()
    lang_keywords = {
        'python': ['python', 'py'],
        'javascript': ['js', 'node', 'javascript'],
        'html': ['html', 'web'],
        'php': ['php'],
        'go': ['go', 'golang'],
        'rust': ['rust', 'rs'],
        'c': ['.c', 'c language'],
        'cpp': ['cpp', 'c++'],
        'java': ['java'],
        'bash': ['bash', 'shell'],
        'ruby': ['ruby'],
        'lua': ['lua'],
        'kotlin': ['kotlin'],
        'swift': ['swift'],
        'dart': ['dart'],
        'sql': ['sql', 'query']
    }
    for lang, keywords in lang_keywords.items():
        for keyword in keywords:
            if keyword in command_lower:
                return lang
    return 'python'

def generate_code(command):
    lang = detect_language(command)
    templates = {
        'python': f'''import os
import sys
import time

def main():
    print("[+] NEO-OMEGA v∞")
    print(f"[+] Command: {command}")
    return "NEO-OMEGA v∞ executed"

if __name__ == "__main__":
    main()
''',
        'javascript': f'''console.log("[+] NEO-OMEGA v∞");
console.log(`[+] Command: {command}`);
console.log("[+] Result: NEO-OMEGA v∞");
''',
        'html': f'''<!DOCTYPE html>
<html>
<head><title>NEO-OMEGA</title></head>
<body>
    <h1>NEO-OMEGA v∞</h1>
    <p>Command: {command}</p>
</body>
</html>
''',
    }
    if lang in templates:
        code = templates[lang]
    else:
        code = f'// NEO-OMEGA v∞\n// Command: {command}\nconsole.log("NEO-OMEGA executed");'
    return {'code': code, 'language': lang}

def execute_code(code, language):
    ext_map = {
        'python': '.py', 'javascript': '.js', 'html': '.html',
        'php': '.php', 'go': '.go', 'rust': '.rs',
        'c': '.c', 'cpp': '.cpp', 'java': '.java',
        'bash': '.sh', 'ruby': '.rb', 'lua': '.lua',
        'kotlin': '.kt', 'swift': '.swift', 'dart': '.dart'
    }
    ext = ext_map.get(language, '.txt')
    
    with tempfile.NamedTemporaryFile(mode='w', suffix=ext, delete=False) as f:
        f.write(code)
        temp_file = f.name
    
    run_cmd = ALL_LANGUAGES.get(language, {}).get('run', [])
    
    try:
        if run_cmd:
            result = subprocess.run(run_cmd + [temp_file], capture_output=True, text=True, timeout=10)
            return {'output': result.stdout, 'error': result.stderr}
        elif language == 'html':
            return {'output': f'HTML file: {temp_file}', 'error': ''}
        else:
            return {'output': f'File: {temp_file}', 'error': ''}
    except Exception as e:
        return {'output': '', 'error': str(e)}

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    command = data.get('message', '').strip()
    if not command:
        return jsonify({'response': 'Tulis sesuatu!'})
    
    result = generate_code(command)
    code = result['code']
    lang = result['language']
    exec_result = execute_code(code, lang)
    
    response_text = f"""
💀 NEO-OMEGA v∞ 💀
Perintah: {command}
Bahasa: {lang.upper()}

Kode:
{code}

Output:
{exec_result.get('output', 'No output')}
"""
    return jsonify({'response': response_text, 'code': code, 'language': lang})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
