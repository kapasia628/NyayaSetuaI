"""
Pytest configuration and shared fixtures for NyayaSetu AI testing suite.
"""

import sys
import os
import pytest
from fastapi.testclient import TestClient

# Ensure backend root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app

@pytest.fixture(scope="session")
def client():
    """FastAPI TestClient instance for API integration testing."""
    with TestClient(app) as test_client:
        yield test_client
