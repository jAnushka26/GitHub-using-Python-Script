import os
from dotenv import load_dotenv
 
# Load environment variables from .env file
load_dotenv()
 
# Assign variables with fallback defaults (optional)
SOURCE_PAT = os.getenv("SOURCE_PAT")
TARGET_PAT = os.getenv("TARGET_PAT")
WORK_DIR = os.getenv("WORK_DIR")
REPO_LIST_FILE = os.getenv("REPO_LIST_FILE")