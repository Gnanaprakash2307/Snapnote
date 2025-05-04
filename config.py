import os
import secrets

# Application settings
DEBUG = True
SECRET_KEY = secrets.token_hex(16)

# Directory settings
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
SAVED_NOTES_FOLDER = os.path.join(BASE_DIR, 'saved_notes')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg'}

# Authentication (for demo purposes - in a real app, use a database)
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'password'

# API Keys (replace with your actual API keys)
GEMINI_API_KEY = "gemini-api-key"  # For summarization
GOOGLE_TRANSLATE_API_KEY = "your-google-translate-key"  # For translation
