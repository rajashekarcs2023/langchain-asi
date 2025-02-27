# tests/conftest.py
import os
import pytest
from dotenv import load_dotenv

# tests/conftest.py
import sys
import os
from pathlib import Path

# Add the project root directory to sys.path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

print(f"Added {project_root} to sys.path")
print(f"sys.path is now: {sys.path}")