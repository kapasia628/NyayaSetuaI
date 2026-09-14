"""
Vercel Serverless Function Entrypoint for NyayaSetu AI FastAPI Backend.
"""

import sys
import os

# Dynamically add the backend folder to Python sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.abspath(os.path.join(current_dir, "..", "backend"))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.main import app
