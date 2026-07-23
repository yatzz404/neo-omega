from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Tambahkan parent directory ke path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import app dari app.py
from app import app as application

# Vercel akan menggunakan 'app' ini
app = application
