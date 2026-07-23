import re
import subprocess
import os
import json
import socket
import platform
import datetime
import random
import math
import requests
from typing import Dict, Any, List, Optional

class AIHandler:
    def __init__(self):
        self.system_info = self._get_system_info()
        self.history = []
        self.max_history = 50
        self.conversation_context = {}
        
    def _get_system_info(self) -> Dict[str, Any]:
        """Get system information"""
        return {
            'os': platform.system(),
            'os_version': platform.version(),
            'machine': platform.machine(),
            'processor': platform.processor(),
            'hostname': socket.gethostname(),
            'python_version': platform.python_version()
        }

    def process_message(self, message: str) -> Dict[str, Any]:
        """Main entry point for processing messages"""
        message_lower = message.lower()
        response_data = {
            'response': '',
            'code': None,
            'output': None,
            'error': None
        }

        # Add to history
        self.history.append(message)
        if len(self.history) > self.max_history:
            self.history.pop(0)

        # Detect and handle different types of requests
        try:
            # Check for code requests first
            if self._is_code_request(message):
                response_data = self._handle_code_request(message, message_lower)
            # Check for system commands
            elif self._is_system_command(message):
                response_data = self._handle_system_command(message)
            # Check for file operations
            elif self._is_file_operation(message):
                response_data = self._handle_file_operation(message)
            # Check for math requests
            elif self._is_math_request(message):
                response_data = self._handle_math_request(message)
            # Check for web requests
            elif self._is_web_request(message):
                response_data = self._handle_web_request(message)
            # Check for date/time requests
            elif self._is_datetime_request(message):
                response_data = self._handle_datetime_request(message)
            # Check for help requests
            elif self._is_help_request(message):
                response_data = self._handle_help_request()
            # General chat
            else:
                response_data = self._handle_general_chat(message)
                
        except Exception as e:
            response_data['error'] = str(e)
            response_data['response'] = f"⚠️ Error processing request: {str(e)}"

        return response_data

    def _is_code_request(self, message: str) -> bool:
        """Check if message requests code"""
        patterns = [
            r'buat(?:kan|lah)?',
            r'bikin(?:in)?',
            r'tulis(?:kan)?',
            r'code',
            r'program',
            r'script',
            r'kode',
            r'fungsi',
            r'function',
            r'class',
            r'python',
            r'javascript',
            r'js',
            r'php',
            r'ruby',
            r'golang',
            r'sql',
            r'html',
            r'css',
            r'generate',
            r'create',
            r'make'
        ]
        return any(re.search(p, message.lower()) for p in patterns)

    def _is_system_command(self, message: str) -> bool:
        """Check if message contains system commands"""
        patterns = [
            r'ls\s|dir\s|cd\s|pwd\s',
            r'ping\s',
            r'whoami',
            r'ipconfig|ifconfig',
            r'netstat',
            r'ps\s|tasklist',
            r'system\s+info',
            r'file\s+info',
            r'shell\s+command',
            r'cmd\s',
            r'hostname',
            r'uptime',
            r'df\s|disk',
            r'free\s|memory'
        ]
        return any(re.search(p, message.lower()) for p in patterns)

    def _is_file_operation(self, message: str) -> bool:
        """Check if message requests file operations"""
        patterns = [
            r'read\s+file',
            r'write\s+file',
            r'create\s+file',
            r'baca\s+file',
            r'tulis\s+file',
            r'save\s+file',
            r'list\s+file',
            r'folder',
            r'directory',
            r'file\s+list',
            r'open\s+file'
        ]
        return any(re.search(p, message.lower()) for p in patterns)

    def _is_math_request(self, message: str) -> bool:
        """Check if message contains mathematical operations"""
        patterns = [
            r'\d+\s*[\+\-\*\/]\s*\d+',
            r'sqrt|akar',
            r'power|pangkat',
            r'log\s*\(',
            r'sin|cos|tan',
            r'calculate|hitung',
            r'mathematics|matematika',
            r'factorial',
            r'percent|persen'
        ]
        return any(re.search(p, message.lower()) for p in patterns)

    def _is_web_request(self, message: str) -> bool:
        """Check if message requests web operations"""
        patterns = [
            r'http',
            r'https',
            r'url',
            r'website',
            r'web\s+scrape',
            r'fetch\s+url',
            r'curl',
            r'request',
            r'api\s+call',
            r'get\s+data\s+from'
        ]
        return any(re.search(p, message.lower()) for p in patterns)

    def _is_datetime_request(self, message: str) -> bool:
        """Check if message requests date/time information"""
        patterns = [
            r'time',
            r'date',
            r'jam',
            r'tanggal',
            r'waktu',
            r'calendar',
            r'kalender',
            r'schedule',
            r'jadwal',
            r'countdown',
            r'timer'
        ]
        return any(re.search(p, message.lower()) for p in patterns)

    def _is_help_request(self, message: str) -> bool:
        """Check if message requests help"""
        patterns = [
            r'help',
            r'bantuan',
            r'tolong',
            r'\?',
            r'what\s+can\s+you',
            r'fitur',
            r'features',
            r'command',
            r'perintah',
            r'capabilities',
            r'ability'
        ]
        return any(re.search(p, message.lower()) for p in patterns)

    def _detect_language(self, message: str) -> str:
        """Detect programming language from message"""
        msg_lower = message.lower()
        if 'python' in msg_lower or 'py' in msg_lower:
            return 'python'
        elif 'javascript' in msg_lower or 'js' in msg_lower:
            return 'javascript'
        elif 'php' in msg_lower:
            return 'php'
        elif 'ruby' in msg_lower:
            return 'ruby'
        elif 'golang' in msg_lower or 'go' in msg_lower:
            return 'golang'
        elif 'sql' in msg_lower:
            return 'sql'
        elif 'html' in msg_lower:
            return 'html'
        elif 'css' in msg_lower:
            return 'css'
        elif 'c++' in msg_lower or 'cpp' in msg_lower:
            return 'cpp'
        elif 'java' in msg_lower:
            return 'java'
        elif 'rust' in msg_lower:
            return 'rust'
        else:
            return 'python'  # Default to Python

    def _handle_code_request(self, message: str, message_lower: str) -> Dict[str, Any]:
        """Generate code based on request"""
        language = self._detect_language(message_lower)
        code = ""
        response = ""
        
        # Detect specific code types
        if 'server' in message_lower or 'web server' in message_lower:
            code = self._generate_web_server_code(language)
            response = f"✅ I've created a complete {language} web server for you!"
        elif 'api' in message_lower and ('rest' in message_lower or 'restful' in message_lower):
            code = self._generate_rest_api_code(language)
            response = f"✅ Here's a complete REST API implementation in {language}!"
        elif 'database' in message_lower or 'db' in message_lower:
            code = self._generate_database_code(language)
            response = f"✅ Database connection and operations code for {language}!"
        elif 'scrape' in message_lower or 'crawl' in message_lower or 'scraping' in message_lower:
            code = self._generate_scraper_code(language)
            response = f"✅ Complete web scraper template in {language}!"
        elif 'function' in message_lower or 'fungsi' in message_lower:
            code = self._generate_function_code(language)
            response = f"✅ Function template with examples in {language}!"
        elif 'class' in message_lower:
            code = self._generate_class_code(language)
            response = f"✅ Class template with complete implementation in {language}!"
        elif 'login' in message_lower or 'authentication' in message_lower:
            code = self._generate_login_code(language)
            response = f"✅ Authentication system code in {language}!"
        elif 'game' in message_lower:
            code = self._generate_game_code(language)
            response = f"✅ Simple game implementation in {language}!"
        elif 'encryption' in message_lower or 'crypto' in message_lower:
            code = self._generate_encryption_code(language)
            response = f"✅ Encryption/decryption code in {language}!"
        else:
            code = self._generate_general_code(language, message)
            response = f"✅ Here's a {language} script based on your request!"

        return {
            'response': response,
            'code': code,
            'output': f"Language: {language.capitalize()}\nGenerated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\nLines: {len(code.splitlines())}"
        }

    def _generate_web_server_code(self, language: str) -> str:
        """Generate web server code"""
        if language == 'python':
            return '''from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return jsonify({
        'status': 'online',
        'message': 'Welcome to NEO-OMEGA Server',
        'timestamp': datetime.now().isoformat(),
        'version': 'v1.0.0'
    })

@app.route('/api/hello', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        data = request.get_json()
        name = data.get('name', 'World')
        return jsonify({
            'message': f'Hello, {name}!',
            'timestamp': datetime.now().isoformat()
        })
    else:
        return jsonify({
            'message': 'Hello, World!',
            'timestamp': datetime.now().isoformat()
        })

@app.route('/api/echo', methods=['POST'])
def echo():
    data = request.get_json()
    return jsonify({
        'echo': data,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/info', methods=['GET'])
def info():
    return jsonify({
        'system': {
            'os': os.name,
            'cwd': os.getcwd(),
            'files': os.listdir('.')[:10]
        },
        'server': {
            'host': request.host,
            'path': request.path,
            'method': request.method
        },
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)'''
        
        elif language == 'javascript':
            return '''const express = require('express');
const cors = require('cors');
const app = express();
const port = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// Routes
app.get('/', (req, res) => {
    res.json({
        status: 'online',
        message: 'Welcome to NEO-OMEGA Server',
        timestamp: new Date().toISOString(),
        version: 'v1.0.0'
    });
});

app.get('/api/hello', (req, res) => {
    res.json({
        message: 'Hello, World!',
        timestamp: new Date().toISOString()
    });
});

app.post('/api/hello', (req, res) => {
    const name = req.body.name || 'World';
    res.json({
        message: `Hello, ${name}!`,
        timestamp: new Date().toISOString()
    });
});

app.post('/api/echo', (req, res) => {
    res.json({
        echo: req.body,
        timestamp: new Date().toISOString()
    });
});

app.get('/api/info', (req, res) => {
    res.json({
        system: {
            platform: process.platform,
            cwd: process.cwd(),
            env: process.env.NODE_ENV
        },
        server: {
            host: req.headers.host,
            path: req.path,
            method: req.method
        },
        timestamp: new Date().toISOString()
    });
});

app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});'''
        
        elif language == 'php':
            return '''<?php
// Simple PHP REST API
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE');
header('Access-Control-Allow-Headers: Content-Type');

function response($data, $status = 200) {
    http_response_code($status);
    echo json_encode($data);
    exit;
}

$method = $_SERVER['REQUEST_METHOD'];
$path = $_SERVER['PATH_INFO'] ?? '/';

// Get request data
$input = json_decode(file_get_contents('php://input'), true);

// Routing
switch($path) {
    case '/':
        response([
            'status' => 'online',
            'message' => 'Welcome to NEO-OMEGA Server',
            'timestamp' => date('c'),
            'version' => 'v1.0.0'
        ]);
        break;
        
    case '/hello':
        if ($method === 'POST') {
            $name = $input['name'] ?? 'World';
            response([
                'message' => "Hello, $name!",
                'timestamp' => date('c')
            ]);
        } else {
            response([
                'message' => 'Hello, World!',
                'timestamp' => date('c')
            ]);
        }
        break;
        
    case '/echo':
        if ($method === 'POST') {
            response([
                'echo' => $input,
                'timestamp' => date('c')
            ]);
        }
        break;
        
    default:
        response(['error' => 'Route not found'], 404);
        break;
}'''
        
        else:
            return f'# Web server code not available for {language}'

    def _generate_rest_api_code(self, language: str) -> str:
        """Generate REST API code"""
        if language == 'python':
            return '''from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# In-memory database
items = [
    {'id': 1, 'name': 'Item 1', 'price': 10.99, 'created_at': '2024-01-01'},
    {'id': 2, 'name': 'Item 2', 'price': 20.99, 'created_at': '2024-01-02'}
]
next_id = 3

@app.route('/api/items', methods=['GET'])
def get_items():
    """Get all items"""
    return jsonify(items)

@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """Get item by ID"""
    item = next((i for i in items if i['id'] == item_id), None)
    if item:
        return jsonify(item)
    return jsonify({'error': 'Item not found'}), 404

@app.route('/api/items', methods=['POST'])
def create_item():
    """Create new item"""
    global next_id
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400
    
    new_item = {
        'id': next_id,
        'name': data['name'],
        'price': data.get('price', 0),
        'created_at': datetime.now().isoformat()
    }
    items.append(new_item)
    next_id += 1
    return jsonify(new_item), 201

@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    """Update item by ID"""
    data = request.get_json()
    item = next((i for i in items if i['id'] == item_id), None)
    
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    
    if 'name' in data:
        item['name'] = data['name']
    if 'price' in data:
        item['price'] = data['price']
    
    return jsonify(item)

@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """Delete item by ID"""
    global items
    item = next((i for i in items if i['id'] == item_id), None)
    
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    
    items = [i for i in items if i['id'] != item_id]
    return jsonify({'message': 'Item deleted successfully'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)'''
        
        else:
            return '# REST API code not available for this language'

    def _generate_database_code(self, language: str) -> str:
        """Generate database code"""
        if language == 'python':
            return '''import sqlite3
from contextlib import contextmanager
from datetime import datetime
from typing import List, Dict, Any

@contextmanager
def get_db():
    """Database connection context manager"""
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    """Initialize database tables"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                active BOOLEAN DEFAULT 1
            )
        ''')
        
        # Products table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                stock INTEGER DEFAULT 0,
                category TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Orders table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                total_price REAL NOT NULL,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
        ''')
        
        conn.commit()
        print("Database initialized successfully!")

class DatabaseManager:
    """Main database operations class"""
    
    @staticmethod
    def create_user(username: str, email: str, password_hash: str, full_name: str = None) -> int:
        """Create a new user"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO users (username, email, password_hash, full_name) VALUES (?, ?, ?, ?)',
                (username, email, password_hash, full_name)
            )
            conn.commit()
            return cursor.lastrowid
    
    @staticmethod
    def get_user(user_id: int) -> Dict[str, Any]:
        """Get user by ID"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
            result = cursor.fetchone()
            return dict(result) if result else None
    
    @staticmethod
    def get_user_by_username(username: str) -> Dict[str, Any]:
        """Get user by username"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            result = cursor.fetchone()
            return dict(result) if result else None
    
    @staticmethod
    def create_product(name: str, price: float, description: str = None, stock: int = 0, category: str = None) -> int:
        """Create a new product"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO products (name, description, price, stock, category) VALUES (?, ?, ?, ?, ?)',
                (name, description, price, stock, category)
            )
            conn.commit()
            return cursor.lastrowid
    
    @staticmethod
    def get_all_products() -> List[Dict[str, Any]]:
        """Get all products"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM products ORDER BY created_at DESC')
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def update_product_stock(product_id: int, quantity: int) -> bool:
        """Update product stock"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE products SET stock = stock - ?, updated_at = CURRENT_TIMESTAMP WHERE id = ? AND stock >= ?',
                (quantity, product_id, quantity)
            )
            conn.commit()
            return cursor.rowcount > 0

# Example usage
if __name__ == '__main__':
    # Initialize database
    init_db()
    
    # Create a user
    user_id = DatabaseManager.create_user(
        username='johndoe',
        email='john@example.com',
        password_hash='hashed_password_here',
        full_name='John Doe'
    )
    print(f"User created with ID: {user_id}")
    
    # Create a product
    product_id = DatabaseManager.create_product(
        name='Laptop',
        price=999.99,
        description='High-performance laptop',
        stock=10,
        category='Electronics'
    )
    print(f"Product created with ID: {product_id}")
    
    # Get all products
    products = DatabaseManager.get_all_products()
    for product in products:
        print(f"{product['name']} - ${product['price']} (Stock: {product['stock']})")'''
        
        else:
            return '# Database code not available for this language'

    def _generate_scraper_code(self, language: str) -> str:
        """Generate web scraper code"""
        if language == 'python':
            return '''import requests
from bs4 import BeautifulSoup
import json
import time
from typing import Dict, List, Any

class WebScraper:
    """Advanced web scraper class"""
    
    def __init__(self, user_agent: str = None):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': user_agent or 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.timeout = 10
    
    def fetch_page(self, url: str) -> str:
        """Fetch page content"""
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch page: {str(e)}")
    
    def parse_html(self, html: str, parser: str = 'html.parser') -> BeautifulSoup:
        """Parse HTML content"""
        return BeautifulSoup(html, parser)
    
    def extract_links(self, soup: BeautifulSoup, base_url: str = None) -> List[str]:
        """Extract all links from page"""
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            if base_url and href.startswith('/'):
                href = base_url + href
            links.append(href)
        return links
    
    def extract_text(self, soup: BeautifulSoup) -> str:
        """Extract clean text from page"""
        for script in soup(["script", "style"]):
            script.decompose()
        return ' '.join(soup.stripped_strings)
    
    def scrape_product(self, url: str) -> Dict[str, Any]:
        """Scrape product information from a product page"""
        html = self.fetch_page(url)
        soup = self.parse_html(html)
        
        # This is a generic template - customize based on the website structure
        product_data = {
            'url': url,
            'title': soup.find('h1').text.strip() if soup.find('h1') else None,
            'price': self._extract_price(soup),
            'description': self._extract_description(soup),
            'images': self._extract_images(soup),
            'reviews': self._extract_reviews(soup),
            'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return product_data
    
    def _extract_price(self, soup: BeautifulSoup) -> float:
        """Extract price from page"""
        price_patterns = [
            r'\$?(\d+\.?\d*)',
            r'Rp\s?(\d+\.?\d*)',
            r'IDR\s?(\d+\.?\d*)'
        ]
        
        for pattern in price_patterns:
            import re
            price_match = re.search(pattern, soup.text)
            if price_match:
                try:
                    return float(price_match.group(1))
                except:
                    pass
        return None
    
    def _extract_description(self, soup: BeautifulSoup) -> str:
        """Extract product description"""
        desc_elements = soup.find_all(['p', 'div'], {'class': ['description', 'product-description', 'desc']})
        if desc_elements:
            return ' '.join([elem.text.strip() for elem in desc_elements[:3]])
        return self.extract_text(soup)[:500]
    
    def _extract_images(self, soup: BeautifulSoup) -> List[str]:
        """Extract image URLs"""
        images = []
        for img in soup.find_all('img', src=True):
            src = img['src']
            if src.startswith('http'):
                images.append(src)
            elif src.startswith('/'):
                images.append('https:' + src)
        return images[:5]  # Limit to 5 images
    
    def _extract_reviews(self, soup: BeautifulSoup) -> int:
        """Extract review count"""
        review_patterns = [
            r'(\d+)\s*review',
            r'(\d+)\s*ulasan',
            r'(\d+)\s*comments'
        ]
        import re
        for pattern in review_patterns:
            match = re.search(pattern, soup.text, re.IGNORECASE)
            if match:
                try:
                    return int(match.group(1))
                except:
                    pass
        return 0

# Example usage
if __name__ == '__main__':
    scraper = WebScraper()
    
    # Example: Scrape a product
    url = 'https://example.com/product-page'
    try:
        product_data = scraper.scrape_product(url)
        print(json.dumps(product_data, indent=2))
    except Exception as e:
        print(f"Error scraping: {e}")'''
        
        else:
            return '# Web scraper code not available for this language'

    def _generate_function_code(self, language: str) -> str:
        """Generate function template"""
        if language == 'python':
            return '''from typing import List, Dict, Any, Optional
from datetime import datetime
import math

def calculate_statistics(data: List[float]) -> Dict[str, float]:
    """
    Calculate comprehensive statistics for a list of numbers.
    
    Args:
        data: List of numbers
    
    Returns:
        Dict containing various statistical measures
    """
    if not data:
        return {'error': 'Empty data provided'}
    
    n = len(data)
    sorted_data = sorted(data)
    
    # Basic statistics
    total = sum(data)
    mean = total / n
    median = sorted_data[n//2] if n % 2 == 1 else (sorted_data[n//2-1] + sorted_data[n//2]) / 2
    
    # Mode
    from collections import Counter
    counter = Counter(data)
    mode = max(counter.items(), key=lambda x: x[1])[0] if counter else None
    
    # Variance and standard deviation
    variance = sum((x - mean) ** 2 for x in data) / n
    std_dev = variance ** 0.5
    
    # Quartiles
    q1 = sorted_data[n//4] if n >= 4 else sorted_data[0]
    q3 = sorted_data[3*n//4] if n >= 4 else sorted_data[-1]
    iqr = q3 - q1
    
    return {
        'count': n,
        'sum': total,
        'mean': mean,
        'median': median,
        'mode': mode,
        'variance': variance,
        'std_dev': std_dev,
        'min': min(data),
        'max': max(data),
        'range': max(data) - min(data),
        'q1': q1,
        'q3': q3,
        'iqr': iqr
    }

def format_number(number: float, precision: int = 2) -> str:
    """Format number with thousand separators"""
    return f"{number:,.{precision}f}"

def clean_text(text: str) -> str:
    """Clean and normalize text"""
    import re
    # Remove extra whitespace
    text = ' '.join(text.split())
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^a-zA-Z0-9\s.,!?\-]', '', text)
    return text.strip()

def extract_emails(text: str) -> List[str]:
    """Extract email addresses from text"""
    import re
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.findall(pattern, text)

def extract_phone_numbers(text: str) -> List[str]:
    """Extract phone numbers from text"""
    import re
    # Simple pattern for Indonesian phone numbers
    patterns = [
        r'\b08\d{8,11}\b',
        r'\b\d{3}-\d{3}-\d{4}\b',
        r'\b\(\d{3}\)\s*\d{3}-\d{4}\b',
        r'\b\+?\d{1,3}\s?\d{9,12}\b'
    ]
    numbers = []
    for pattern in patterns:
        numbers.extend(re.findall(pattern, text))
    return list(set(numbers))

# Example usage
if __name__ == '__main__':
    # Test statistics
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    stats = calculate_statistics(numbers)
    print("Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Test text processing
    text = "  Hello,   World!   Visit me@example.com   "
    print(f"\\nCleaned: {clean_text(text)}")
    print(f"Emails: {extract_emails(text)}")
    print(f"Format: {format_number(1234567.89)}")'''
        
        else:
            return '# Function template not available for this language'

    def _generate_class_code(self, language: str) -> str:
        """Generate class template"""
        if language == 'python':
            return '''from datetime import datetime
from typing import List, Optional, Dict, Any
import json

class User:
    """User class with complete CRUD operations"""
    
    def __init__(self, user_id: int, username: str, email: str, full_name: Optional[str] = None):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.full_name = full_name
        self.created_at = datetime.now()
        self.last_login = None
        self.active = True
        self.permissions = []
    
    def login(self) -> None:
        """Record user login"""
        self.last_login = datetime.now()
    
    def update_email(self, new_email: str) -> bool:
        """Update user's email with validation"""
        if '@' not in new_email or '.' not in new_email:
            return False
        self.email = new_email
        return True
    
    def add_permission(self, permission: str) -> None:
        """Add a permission to user"""
        if permission not in self.permissions:
            self.permissions.append(permission)
    
    def has_permission(self, permission: str) -> bool:
        """Check if user has specific permission"""
        return permission in self.permissions
    
    def deactivate(self) -> None:
        """Deactivate user account"""
        self.active = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert user to dictionary"""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'created_at': self.created_at.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'active': self.active,
            'permissions': self.permissions
        }
    
    def to_json(self) -> str:
        """Convert user to JSON"""
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        """Create User from dictionary"""
        user = cls(
            user_id=data['user_id'],
            username=data['username'],
            email=data['email'],
            full_name=data.get('full_name')
        )
        user.active = data.get('active', True)
        user.permissions = data.get('permissions', [])
        return user

class UserManager:
    """Manager class for User operations"""
    
    def __init__(self):
        self._users: List[User] = []
        self._next_id: int = 1
    
    def create_user(self, username: str, email: str, full_name: Optional[str] = None) -> User:
        """Create a new user"""
        user = User(self._next_id, username, email, full_name)
        self._users.append(user)
        self._next_id += 1
        return user
    
    def get_user(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        for user in self._users:
            if user.user_id == user_id:
                return user
        return None
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        for user in self._users:
            if user.username == username:
                return user
        return None
    
    def get_all_users(self) -> List[User]:
        """Get all users"""
        return self._users.copy()
    
    def get_active_users(self) -> List[User]:
        """Get only active users"""
        return [user for user in self._users if user.active]
    
    def delete_user(self, user_id: int) -> bool:
        """Delete user by ID"""
        user = self.get_user(user_id)
        if user:
            self._users.remove(user)
            return True
        return False
    
    def search_users(self, query: str) -> List[User]:
        """Search users by username or email"""
        query = query.lower()
        return [
            user for user in self._users
            if query in user.username.lower() or 
               query in user.email.lower() or
               (user.full_name and query in user.full_name.lower())
        ]
    
    def to_dict(self) -> List[Dict[str, Any]]:
        """Convert all users to list of dictionaries"""
        return [user.to_dict() for user in self._users]

# Example usage
if __name__ == '__main__':
    manager = UserManager()
    
    # Create users
    user1 = manager.create_user('johndoe', 'john@example.com', 'John Doe')
    user2 = manager.create_user('janesmith', 'jane@example.com', 'Jane Smith')
    
    # Add permissions
    user1.add_permission('admin')
    user1.add_permission('write')
    user2.add_permission('read')
    
    # Login user
    user1.login()
    
    # Search users
    results = manager.search_users('john')
    for user in results:
        print(user.to_json())'''
        
        else:
            return '# Class template not available for this language'

    def _generate_login_code(self, language: str) -> str:
        """Generate login/authentication code"""
        if language == 'python':
            return '''from flask import Flask, request, jsonify, session
from flask_cors import CORS
import hashlib
import secrets
from datetime import datetime, timedelta
import jwt

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
CORS(app)

# In-memory user database
users = {}
tokens = {}

def hash_password(password: str) -> str:
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    return hash_password(password) == hashed

@app.route('/api/register', methods=['POST'])
def register():
    """User registration endpoint"""
    data = request.get_json()
    
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Username and password required'}), 400
    
    username = data['username']
    password = data['password']
    
    if username in users:
        return jsonify({'error': 'Username already exists'}), 400
    
    # Store user
    users[username] = {
        'username': username,
        'password_hash': hash_password(password),
        'created_at': datetime.now().isoformat(),
        'email': data.get('email', '')
    }
    
    return jsonify({
        'message': 'User registered successfully',
        'username': username
    }), 201

@app.route('/api/login', methods=['POST'])
def login():
    """User login endpoint"""
    data = request.get_json()
    
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Username and password required'}), 400
    
    username = data['username']
    password = data['password']
    
    if username not in users:
        return jsonify({'error': 'Invalid username or password'}), 401
    
    user = users[username]
    if not verify_password(password, user['password_hash']):
        return jsonify({'error': 'Invalid username or password'}), 401
    
    # Generate token
    token = secrets.token_hex(32)
    tokens[token] = {
        'username': username,
        'created_at': datetime.now(),
        'expires_at': datetime.now() + timedelta(hours=24)
    }
    
    return jsonify({
        'message': 'Login successful',
        'username': username,
        'token': token,
        'expires_in': 86400  # 24 hours in seconds
    })

@app.route('/api/profile', methods=['GET'])
def profile():
    """Get user profile (requires authentication)"""
    token = request.headers.get('Authorization')
    
    if not token or not token.startswith('Bearer '):
        return jsonify({'error': 'Authorization header required'}), 401
    
    token = token.split(' ')[1]
    
    if token not in tokens:
        return jsonify({'error': 'Invalid token'}), 401
    
    token_data = tokens[token]
    if token_data['expires_at'] < datetime.now():
        del tokens[token]
        return jsonify({'error': 'Token expired'}), 401
    
    username = token_data['username']
    user = users[username]
    
    return jsonify({
        'username': user['username'],
        'email': user.get('email', ''),
        'created_at': user['created_at']
    })

@app.route('/api/logout', methods=['POST'])
def logout():
    """User logout endpoint"""
    token = request.headers.get('Authorization')
    
    if token and token.startswith('Bearer '):
        token = token.split(' ')[1]
        if token in tokens:
            del tokens[token]
    
    return jsonify({'message': 'Logged out successfully'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)'''
        
        else:
            return '# Login code not available for this language'

    def _generate_game_code(self, language: str) -> str:
        """Generate game code"""
        if language == 'python':
            return '''import random
import time

class NumberGuessingGame:
    """A simple number guessing game"""
    
    def __init__(self, min_num: int = 1, max_num: int = 100, max_attempts: int = 10):
        self.min_num = min_num
        self.max_num = max_num
        self.max_attempts = max_attempts
        self.secret_number = random.randint(min_num, max_num)
        self.attempts = 0
        self.guesses = []
        self.game_over = False
    
    def guess(self, number: int) -> str:
        """Make a guess"""
        if self.game_over:
            return "Game is already over! Start a new game."
        
        if number < self.min_num or number > self.max_num:
            return f"Please guess a number between {self.min_num} and {self.max_num}"
        
        self.attempts += 1
        self.guesses.append(number)
        
        if number == self.secret_number:
            self.game_over = True
            return f"🎉 Congratulations! You found the number {self.secret_number} in {self.attempts} attempts!"
        
        if self.attempts >= self.max_attempts:
            self.game_over = True
            return f"❌ Game Over! The number was {self.secret_number}. Better luck next time!"
        
        if number < self.secret_number:
            return f"🔼 Too low! Try higher. ({self.attempts}/{self.max_attempts})"
        else:
            return f"🔽 Too high! Try lower. ({self.attempts}/{self.max_attempts})"
    
    def get_hint(self) -> str:
        """Get a hint"""
        if self.game_over:
            return "Game is over! Start a new game."
        
        # Give some clue about the number
        if self.secret_number % 2 == 0:
            return "💡 The number is even"
        else:
            return "💡 The number is odd"
    
    def get_status(self) -> dict:
        """Get game status"""
        return {
            'attempts': self.attempts,
            'max_attempts': self.max_attempts,
            'guesses': self.guesses,
            'range': f'{self.min_num}-{self.max_num}',
            'game_over': self.game_over
        }
    
    def reset(self):
        """Reset the game"""
        self.secret_number = random.randint(self.min_num, self.max_num)
        self.attempts = 0
        self.guesses = []
        self.game_over = False

# Example usage
if __name__ == '__main__':
    game = NumberGuessingGame(1, 50, 7)
    print("🎮 Welcome to Number Guessing Game!")
    print(f"Guess a number between {game.min_num} and {game.max_num}")
    print(f"You have {game.max_attempts} attempts")
    
    while not game.game_over:
        try:
            guess = int(input("\\nEnter your guess: "))
            result = game.guess(guess)
            print(result)
            
            if not game.game_over:
                print(game.get_hint())
        except ValueError:
            print("Please enter a valid number!")
    
    print(f"\\nGame Statistics: {game.get_status()}")'''
        
        else:
            return '# Game code not available for this language'

    def _generate_encryption_code(self, language: str) -> str:
        """Generate encryption code"""
        if language == 'python':
            return '''import hashlib
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class EncryptionManager:
    """Advanced encryption and hashing utilities"""
    
    def __init__(self):
        self.salt = b'neo_omega_salt_2024'
    
    def generate_key(self, password: str) -> bytes:
        """Generate encryption key from password"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    def encrypt_text(self, text: str, password: str) -> str:
        """Encrypt text with password"""
        key = self.generate_key(password)
        f = Fernet(key)
        encrypted = f.encrypt(text.encode())
        return base64.urlsafe_b64encode(encrypted).decode()
    
    def decrypt_text(self, encrypted_text: str, password: str) -> str:
        """Decrypt text with password"""
        key = self.generate_key(password)
        f = Fernet(key)
        try:
            decrypted = f.decrypt(base64.urlsafe_b64decode(encrypted_text))
            return decrypted.decode()
        except Exception as e:
            raise Exception(f"Decryption failed: {str(e)}")
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def hash_file(self, file_path: str, algorithm: str = 'sha256') -> str:
        """Calculate file hash"""
        hash_func = hashlib.new(algorithm)
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hash_func.update(chunk)
        return hash_func.hexdigest()
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        return self.hash_password(password) == hashed
    
    def generate_otp(self, length: int = 6) -> str:
        """Generate OTP (One-Time Password)"""
        import random
        return ''.join(str(random.randint(0, 9)) for _ in range(length))
    
    def xor_encrypt_decrypt(self, text: str, key: str) -> str:
        """XOR encryption/decryption (symmetric)"""
        result = []
        for i, char in enumerate(text):
            result.append(chr(ord(char) ^ ord(key[i % len(key)])))
        return ''.join(result)

# Example usage
if __name__ == '__main__':
    em = EncryptionManager()
    
    # Password hashing
    password = "my_secure_password"
    hashed = em.hash_password(password)
    print(f"Password hash: {hashed}")
    print(f"Password valid: {em.verify_password(password, hashed)}")
    
    # Text encryption
    text = "This is a secret message"
    password = "secret_key_2024"
    encrypted = em.encrypt_text(text, password)
    print(f"Encrypted: {encrypted}")
    decrypted = em.decrypt_text(encrypted, password)
    print(f"Decrypted: {decrypted}")
    
    # OTP generation
    otp = em.generate_otp(6)
    print(f"OTP: {otp}")
    
    # XOR encryption
    xor_encrypted = em.xor_encrypt_decrypt(text, "key")
    print(f"XOR encrypted: {xor_encrypted}")
    xor_decrypted = em.xor_encrypt_decrypt(xor_encrypted, "key")
    print(f"XOR decrypted: {xor_decrypted}")'''
        
        else:
            return '# Encryption code not available for this language'

    def _generate_general_code(self, language: str, message: str) -> str:
        """Generate general code based on message"""
        if language == 'python':
            return f'''#!/usr/bin/env python3
"""
NEO-OMEGA v∞ Code Generator
Request: {message[:100]}...
Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

import os
import sys
from datetime import datetime

def main():
    print("=" * 50)
    print("🚀 NEO-OMEGA v∞ Code Generator")
    print("=" * 50)
    print(f"📝 Request: {message}")
    print(f"⏰ Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"💻 Language: {language.capitalize()}")
    print("=" * 50)
    print()
    
    # === YOUR CODE STARTS HERE ===
    # TODO: Implement your logic based on the request
    
    print("✅ Code generated successfully!")
    print("📌 Tip: Customize this code to fit your specific needs")
    
    # Example output
    print("\\n📊 Example Output:")
    print("-" * 30)
    print("Hello from NEO-OMEGA!")
    print("-" * 30)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\\n⚠️ Process interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\\n❌ Error: {str(e)}")
        sys.exit(1)'''
        else:
            return f'''// NEO-OMEGA v∞ Code Generator
// Request: {message[:50]}...
// Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
// Language: {language.capitalize()}

// TODO: Implement your logic here
console.log("Hello from NEO-OMEGA!");'''

    def _handle_system_command(self, message: str) -> Dict[str, Any]:
        """Handle system commands"""
        # Security: Only allow safe commands
        safe_commands = ['ls', 'dir', 'pwd', 'cd', 'whoami', 'hostname', 'uptime', 'date']
        
        # Parse command
        command_parts = message.split()
        
        if command_parts and command_parts[0].lower() in safe_commands:
            try:
                # For 'date' command, use Python instead of shell
                if command_parts[0].lower() == 'date':
                    return {
                        'response': f"✅ Current date and time:\n\n```\n{datetime.datetime.now().strftime('%A, %B %d, %Y %H:%M:%S')}\n```",
                        'output': datetime.datetime.now().isoformat()
                    }
                
                # For 'pwd', get current directory
                if command_parts[0].lower() == 'pwd':
                    return {
                        'response': f"✅ Current directory:\n\n```\n{os.getcwd()}\n```",
                        'output': os.getcwd()
                    }
                
                result = subprocess.run(
                    command_parts,
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                output = result.stdout if result.stdout else result.stderr
                return {
                    'response': f"✅ Command executed successfully!\n\n```\n{output}\n```",
                    'output': output
                }
            except subprocess.TimeoutExpired:
                return {
                    'response': "⏰ Command timed out. Please try a simpler command.",
                    'error': 'Timeout'
                }
            except Exception as e:
                return {
                    'response': f"⚠️ Failed to execute command: {str(e)}",
                    'error': str(e)
                }
        else:
            # Provide system info instead
            return {
                'response': f"""📊 **System Information**

🖥️ **OS**: {self.system_info['os']}
📦 **Version**: {self.system_info['os_version']}
🔧 **Machine**: {self.system_info['machine']}
💻 **Hostname**: {self.system_info['hostname']}
🐍 **Python**: {self.system_info['python_version']}

💡 **Tip**: You can run safe commands like: `ls`, `pwd`, `whoami`, `hostname`
⚠️ **Security**: Only safe system info commands are allowed.""",
                'output': json.dumps(self.system_info, indent=2)
            }

    def _handle_file_operation(self, message: str) -> Dict[str, Any]:
        """Handle file operations"""
        response = "📁 **File Operations**\n\n"
        response += "**Available Operations:**\n"
        response += "• `list files` - List files in current directory\n"
        response += "• `read file [filename]` - Read file content\n"
        response += "• `create file [filename]` - Create new file\n\n"
        response += "**Security Notice:**\n"
        response += "• Only current directory access\n"
        response += "• No file deletion allowed\n"
        response += "• Limited to text files\n\n"
        
        # Try to list files if requested
        if 'list' in message.lower() or 'ls' in message.lower():
            try:
                files = os.listdir('.')
                file_list = "\n".join([f"• `{f}`" for f in files[:20]])
                if len(files) > 20:
                    file_list += f"\n• ... and {len(files) - 20} more files"
                response += f"**📂 Files in current directory ({len(files)} files):**\n{file_list}"
            except Exception as e:
                response += f"⚠️ Error listing files: {str(e)}"
        
        # Try to read file if requested
        elif 'read' in message.lower():
            import re
            file_match = re.search(r'read\s+file\s+(\S+)', message.lower())
            if file_match:
                filename = file_match.group(1)
                try:
                    with open(filename, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Limit output size
                        if len(content) > 2000:
                            content = content[:2000] + "\n... (truncated)"
                        response += f"**📄 Reading file: `{filename}`**\n\n```\n{content}\n```"
                except FileNotFoundError:
                    response += f"⚠️ File `{filename}` not found"
                except Exception as e:
                    response += f"⚠️ Error reading file: {str(e)}"
        
        # Try to create file if requested
        elif 'create' in message.lower():
            import re
            file_match = re.search(r'create\s+file\s+(\S+)', message.lower())
            if file_match:
                filename = file_match.group(1)
                try:
                    # Check if it's a Python file request
                    content = f"# File created by NEO-OMEGA at {datetime.datetime.now()}\n\n# TODO: Add your content here\n"
                    if filename.endswith('.py'):
                        content = f'''#!/usr/bin/env python3
"""File created by NEO-OMEGA at {datetime.datetime.now()}"""

def main():
    print("Hello from {filename}!")

if __name__ == "__main__":
    main()
'''
                    elif filename.endswith('.js'):
                        content = f'''// File created by NEO-OMEGA at {datetime.datetime.now()}
console.log("Hello from {filename}!");'''
                    elif filename.endswith('.html'):
                        content = f'''<!DOCTYPE html>
<html>
<head>
    <title>{filename}</title>
    <meta charset="UTF-8">
</head>
<body>
    <h1>Hello from {filename}</h1>
    <p>Created by NEO-OMEGA at {datetime.datetime.now()}</p>
</body>
</html>'''
                    
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(content)
                    response += f"✅ File `{filename}` created successfully!\n\n```\n{content}\n```"
                except Exception as e:
                    response += f"⚠️ Error creating file: {str(e)}"
        
        return {
            'response': response,
            'output': 'File operations completed'
        }

    def _handle_math_request(self, message: str) -> Dict[str, Any]:
        """Handle mathematical operations"""
        try:
            # Extract mathematical expression
            expression = re.search(r'[\d\+\-\*\/\(\)\.]+', message)
            if expression:
                expr = expression.group()
                # Safe eval with math functions
                safe_dict = {
                    'sqrt': math.sqrt,
                    'sin': math.sin,
                    'cos': math.cos,
                    'tan': math.tan,
                    'log': math.log,
                    'log10': math.log10,
                    'pow': math.pow,
                    'pi': math.pi,
                    'e': math.e,
                    'factorial': math.factorial,
                    'abs': abs,
                    'round': round,
                    'ceil': math.ceil,
                    'floor': math.floor
                }
                result = eval(expr, {"__builtins__": {}}, safe_dict)
                
                # Format result
                if isinstance(result, float):
                    if result.is_integer():
                        result = int(result)
                    else:
                        result = round(result, 6)
                
                return {
                    'response': f"🧮 **Math Result**\n\n`{expr}` = **{result}**\n\n✅ Calculation completed successfully!",
                    'output': str(result)
                }
            else:
                # Check for specific math keywords
                if 'sqrt' in message.lower() or 'akar' in message.lower():
                    number = re.search(r'\d+', message)
                    if number:
                        num = float(number.group())
                        result = math.sqrt(num)
                        return {
                            'response': f"🧮 **Square Root**\n\n√{num} = **{result}**",
                            'output': str(result)
                        }
                elif 'factorial' in message.lower():
                    number = re.search(r'\d+', message)
                    if number:
                        num = int(number.group())
                        result = math.factorial(num)
                        return {
                            'response': f"🧮 **Factorial**\n\n{num}! = **{result}**",
                            'output': str(result)
                        }
                elif 'power' in message.lower() or 'pangkat' in message.lower():
                    numbers = re.findall(r'\d+', message)
                    if len(numbers) >= 2:
                        base = float(numbers[0])
                        exp = float(numbers[1])
                        result = base ** exp
                        return {
                            'response': f"🧮 **Power**\n\n{base}^{exp} = **{result}**",
                            'output': str(result)
                        }
                
                return {
                    'response': "⚠️ No valid mathematical expression found.\n\n**Examples:**\n• `2 + 2`\n• `sqrt(16)`\n• `sin(30)`\n• `factorial(5)`\n• `power(2, 8)`",
                    'error': 'No expression found'
                }
        except Exception as e:
            return {
                'response': f"⚠️ Error calculating: {str(e)}",
                'error': str(e)
            }

    def _handle_web_request(self, message: str) -> Dict[str, Any]:
        """Handle web requests"""
        try:
            # Extract URL
            url_pattern = r'https?://[^\s]+'
            url_match = re.search(url_pattern, message)
            
            if url_match:
                url = url_match.group()
                try:
                    response = requests.get(url, timeout=10, headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                    })
                    response.raise_for_status()
                    
                    content_type = response.headers.get('content-type', '')
                    if 'json' in content_type:
                        data = response.json()
                        return {
                            'response': f"✅ **JSON Data Fetched**\n\nURL: {url}\nStatus: {response.status_code}",
                            'output': json.dumps(data, indent=2)[:2000]
                        }
                    else:
                        # Return first 1000 chars
                        text_preview = response.text[:1000] + ('...' if len(response.text) > 1000 else '')
                        return {
                            'response': f"✅ **Content Fetched**\n\nURL: {url}\nStatus: {response.status_code}\nContent Type: {content_type}\n\n**Preview:**",
                            'output': text_preview
                        }
                except requests.exceptions.Timeout:
                    return {
                        'response': f"⏰ Request to {url} timed out. The website might be slow or unreachable.",
                        'error': 'Timeout'
                    }
                except requests.exceptions.ConnectionError:
                    return {
                        'response': f"🔌 Could not connect to {url}. Check the URL or your internet connection.",
                        'error': 'Connection error'
                    }
                except requests.exceptions.HTTPError as e:
                    return {
                        'response': f"❌ HTTP Error: {str(e)}",
                        'error': str(e)
                    }
                except Exception as e:
                    return {
                        'response': f"⚠️ Failed to fetch {url}: {str(e)}",
                        'error': str(e)
                    }
            else:
                return {
                    'response': "🌐 **Web Operations**\n\nI can help you fetch web content!\n\n**Usage:**\n• `fetch https://example.com` - Get website content\n• `scrape https://example.com` - Scrape website data\n• `api https://api.example.com` - Call API endpoint\n\n**Example:** `fetch https://jsonplaceholder.typicode.com/posts/1`",
                    'error': 'No URL found'
                }
        except Exception as e:
            return {
                'response': f"⚠️ Error processing web request: {str(e)}",
                'error': str(e)
            }

    def _handle_datetime_request(self, message: str) -> Dict[str, Any]:
        """Handle date/time requests"""
        now = datetime.datetime.now()
        response = "📅 **Date & Time Information**\n\n"
        response += f"📆 **Date**: `{now.strftime('%A, %B %d, %Y')}`\n"
        response += f"🕐 **Time**: `{now.strftime('%H:%M:%S')}`\n"
        response += f"🌍 **Timezone**: `{datetime.datetime.now().astimezone().tzinfo}`\n"
        response += f"📋 **ISO**: `{now.isoformat()}`\n"
        response += f"🔢 **Unix Timestamp**: `{int(now.timestamp())}`\n"
        
        # Add calendar if requested
        if 'calendar' in message.lower() or 'kalender' in message.lower():
            import calendar
            cal = calendar.month(now.year, now.month)
            response += f"\n**📅 Calendar for {now.strftime('%B %Y')}:**\n```\n{cal}\n```"
        
        # Add countdown if requested
        if 'countdown' in message.lower():
            target = None
            if 'tomorrow' in message.lower():
                target = now + datetime.timedelta(days=1)
                target = target.replace(hour=0, minute=0, second=0, microsecond=0)
            elif 'new year' in message.lower():
                target = datetime.datetime(now.year + 1, 1, 1, 0, 0, 0)
            elif 'christmas' in message.lower() or 'natal' in message.lower():
                target = datetime.datetime(now.year, 12, 25, 0, 0, 0)
                if target < now:
                    target = target.replace(year=now.year + 1)
            
            if target:
                diff = target - now
                days = diff.days
                hours = diff.seconds // 3600
                minutes = (diff.seconds // 60) % 60
                seconds = diff.seconds % 60
                response += f"\n⏳ **Countdown to {target.strftime('%B %d, %Y')}:**\n"
                response += f"**{days} days, {hours} hours, {minutes} minutes, {seconds} seconds**"
        
        return {
            'response': response,
            'output': now.isoformat()
        }

    def _handle_help_request(self) -> Dict[str, Any]:
        """Handle help requests"""
        help_text = """**🤖 NEO-OMEGA v∞ — OMNIBREAKER**

**💻 Code Generation:**
• `buat web server python` - Generate Flask/Express server
• `bikin rest api` - Generate REST API
• `buat database python` - Database connection code
• `scrape website` - Web scraper template
• `bikin function` - Function template
• `buat class` - Class template
• `bikin login` - Authentication system
• `buat game` - Simple game
• `encryption` - Encryption utilities

**🛠️ System Commands:**
• `ls` / `dir` - List files
• `pwd` - Show current directory
• `whoami` - Show user
• `hostname` - Show hostname
• `system info` - Show system information

**📁 File Operations:**
• `list files` - List files in directory
• `read file [name]` - Read file content
• `create file [name]` - Create new file

**🧮 Math Operations:**
• `2 + 2` - Basic arithmetic
• `sqrt(16)` - Square root
• `sin(30)` - Trigonometry
• `factorial(5)` - Factorial
• `power(2, 8)` - Power

**🌐 Web Operations:**
• `fetch https://example.com` - Fetch website content
• `scrape https://example.com` - Scrape data

**📅 Date & Time:**
• `time` - Show current time
• `date` - Show current date
• `calendar` - Show monthly calendar
• `countdown` - Show countdown

**💡 Tips:**
• Be specific about what you want
• Specify programming language (Python, JS, PHP, etc.)
• I support: Python, JavaScript, PHP, Ruby, Go, SQL, HTML, CSS
• For safety, I can't execute destructive commands

*Always ready to help you code!* 🔥"""
        
        return {'response': help_text}

    def _handle_general_chat(self, message: str) -> Dict[str, Any]:
        """Handle general chat messages"""
        message_lower = message.lower()
        
        # Check for specific queries
        if 'nama' in message_lower or 'name' in message_lower:
            return {'response': "🤖 I'm **NEO-OMEGA v∞ OMNIBREAKER**, your advanced AI assistant!"}
        
        if 'kabar' in message_lower or 'how are you' in message_lower:
            return {'response': "💪 I'm running at peak performance and ready to help you code! What can I assist you with today?"}
        
        if 'makasih' in message_lower or 'terima kasih' in message_lower or 'thanks' in message_lower:
            return {'response': "🚀 You're welcome! Always happy to help. Feel free to ask anything else!"}
        
        if 'siapa' in message_lower or 'who' in message_lower:
            return {'response': "🤖 I'm NEO-OMEGA, an AI assistant specialized in coding, system operations, and general knowledge. I'm here to help you build amazing things!"}
        
        if 'bisa' in message_lower and ('apa' in message_lower or 'what' in message_lower):
            return {'response': """**💡 What I Can Do:**
            
1. **Generate Code** - Create scripts in various languages
2. **Run System Commands** - Safe system info retrieval
3. **File Operations** - List, read, and create files
4. **Math Calculations** - Complex mathematical operations
5. **Web Operations** - Fetch and scrape web content
6. **Date & Time** - Current time, date, and calendar

Just type `help` for the complete list of commands! 🚀"""}
        
        if 'coding' in message_lower or 'programming' in message_lower:
            return {'response': """💻 **Let's Code Together!**

I can help you with:
• Building web applications
• Creating REST APIs
• Database management
• Web scraping
• Game development
• Authentication systems
• Encryption utilities

Just tell me what you want to build and I'll provide the code! 🚀"""}
        
        # Default response
        responses = [
            "🤖 I'm NEO-OMEGA, your AI assistant. How can I help you code today?",
            "💻 Ready to help with your coding needs. What would you like to build?",
            "🚀 I'm here to assist! Try saying 'help' to see what I can do.",
            "✨ Let's create something amazing! What code do you need?",
            "💪 Your AI coding assistant is ready. How can I help?",
        ]
        
        return {
            'response': random.choice(responses) + " 🔥"
        }
