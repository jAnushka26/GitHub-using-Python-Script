
from dotenv import load_dotenv
import os
 
# Load environment variables from .env
load_dotenv()
 
# Read GitHub credentials
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
 
# Basic validation
if not GITHUB_USERNAME or not GITHUB_TOKEN:
    raise Exception("Missing GITHUB_USERNAME or GITHUB_TOKEN in .env file")
 