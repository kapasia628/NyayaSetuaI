"""
Application Configuration for NyayaSetu AI.
Enterprise-grade legal technology platform adhering to OWASP and Indian Legal Compliance standards.
"""

import os
from typing import List

class Settings:
    PROJECT_NAME: str = "NyayaSetu AI"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "AI for Legal Assistance & Access - Empowering citizens with accessible, secure, trilingual legal intelligence."
    API_V1_STR: str = "/api"
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "production")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # LLM API Keys (Optional - platform works fully offline via built-in engine)
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # Security & CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost",
        "http://localhost:8000",
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1",
        "http://127.0.0.1:8000",
        "*"
    ]
    
    # Supported Languages: English, Hindi, Gujarati
    SUPPORTED_LANGUAGES: List[str] = ["en", "hi", "gu"]
    DEFAULT_LANGUAGE: str = "en"
    
    # Rate Limiting
    RATE_LIMIT_DEFAULT: str = "60/minute"

settings = Settings()
