import time, subprocess, sys, os
BASE = os.path.dirname(os.path.abspath(__file__))
CMD = [os.path.join(BASE, "venv/bin/python"), os.path.join(BASE, "ingest_outlook_imap_to_postgres.py")]

while True:
    print("▶︎ Running ingest...")
    try:
        subprocess.run(CMD, check=False)
    except Exception as e:
        print("ERROR:", e)
    time.sleep(120)  # poll every 2 minutes
