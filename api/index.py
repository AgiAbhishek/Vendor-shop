import os, sys
from pathlib import Path
import serverless_wsgi

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

from project.wsgi import application  # noqa

def handler(event, context):
    return serverless_wsgi.handle_request(application, event, context)
