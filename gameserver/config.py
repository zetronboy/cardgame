import os
"""
program settings and flask options
"""
TESTING = bool(os.getenv('TESTING')) or True
FLASK_DEBUG = bool(os.getenv('FLASK_DEBUG')) or True
SECRET_KEY = os.getenv('SECRET_KEY') or "1234567890poiuytrewqasdfghjkl"
SERVER = os.getenv('SERVER') or "127.0.0.1"