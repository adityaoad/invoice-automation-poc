import time, subprocess, os

BASE = os.path.dirname(os.path.abspath(__file__))
CMD = [os.path.join(BASE, "venv/bin/python"), os.path.join(BASE, "ingest_outlook_imap_to_postgres.py")]

end_time = time.time() + 15*60  # 15 minutes from now

while time.time() < end_time:
    print("▶︎ Running ingest...")
    try:
        subprocess.run(CMD, check=False)
    except Exception as e:
        print("ERROR:", e)
    time.sleep(120)  # poll every 2 minutes

print("⏹️ Runner finished after 15 minutes.")
