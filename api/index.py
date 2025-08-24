import os
import sys
from pathlib import Path
import serverless_wsgi  # <-- use serverless-wsgi instead of vercel-wsgi

# Add the backend folder to PYTHONPATH
ROOT = Path(__file__).resolve().parents[1]  # repo root
BACKEND = ROOT / "backend"
sys.path.insert(0, str(BACKEND))

# Point to Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

# Import the Django WSGI application
from project.wsgi import application  # noqa: E402

def handler(event, context):
    """Vercel serverless entrypoint for Django via serverless-wsgi"""
    return serverless_wsgi.handle_request(application, event, context)
