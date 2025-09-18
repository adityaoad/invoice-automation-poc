from imapclient import IMAPClient
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("GMAIL_EMAIL")
PWD   = os.getenv("GMAIL_APP_PASSWORD")
HOST  = os.getenv("IMAP_HOST", "outlook.office365.com")

print("🔍 Trying login with:", EMAIL)
print("IMAP host:", HOST)

with IMAPClient(HOST, port=993, ssl=True) as server:
    server.login(EMAIL, PWD)
    print("✅ Login successful")
    print("Available folders:", server.list_folders())
