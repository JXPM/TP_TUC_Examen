"""Pytest configuration - ensure project root is in sys.path."""
import sys
import os

# Add project root to path so 'app' is importable directly
sys.path.insert(0, os.path.dirname(__file__))
