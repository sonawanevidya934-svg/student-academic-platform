"""Application configuration."""
import os
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')
class Config:
    DATABASE = os.environ.get('SAP_DATABASE', os.path.join(INSTANCE_DIR, 'app.db'))
    MAX_CREDITS_PER_SEMESTER = 18
    TESTING = False
