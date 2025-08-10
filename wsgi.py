"""
WSGI configuration for PythonAnywhere deployment
"""

import sys
import os

# Add the project directory to Python path
project_home = '/home/yourusername/investment-simulation'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variables
os.environ.setdefault('PYTHONPATH', project_home)

# Import the FastAPI app
from backend.api import app

# PythonAnywhere expects 'application' variable
application = app