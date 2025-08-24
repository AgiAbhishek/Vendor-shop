import os
import sys
from pathlib import Path
from vercel_wsgi import handle

# Add the backend folder to PYTHONPATH
ROOT = Path(__file__).resolve().parents[1]  # repo root
BACKEND = ROOT / "backend"
sys.path.insert(0, str(BACKEND))

# Point to Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

# Import the Django WSGI application
from project.wsgi import application  # noqa: E402

def handler(event, context):
    """Vercel serverless entrypoint for Django"""
    return handle(event, context, application)
