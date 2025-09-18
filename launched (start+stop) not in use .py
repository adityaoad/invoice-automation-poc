<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>com.invoice.ingest</string>
  <key>ProgramArguments</key>
  <array>
    <string>/Users/adityasmacbookair/Documents/Invoice Automation Project/venv/bin/python</string>
    <string>/Users/adityasmacbookair/Documents/Invoice Automation Project/ingest_outlook_imap_to_postgres.py</string>
  </array>
  <key>WorkingDirectory</key><string>/Users/adityasmacbookair/Documents/Invoice Automation Project</string>
  <key>StartInterval</key><integer>120</integer> <!-- every 2 minutes -->
  <key>StandardOutPath</key><string>/Users/adityasmacbookair/Documents/Invoice Automation Project/ingest.out.log</string>
  <key>StandardErrorPath</key><string>/Users/adityasmacbookair/Documents/Invoice Automation Project/ingest.err.log</string>
  <key>EnvironmentVariables</key>
  <dict>
    <key>PYTHONUNBUFFERED</key><string>1</string>
  </dict>
</dict>
</plist>




launchctl load ~/Library/LaunchAgents/com.invoice.ingest.plist
launchctl start com.invoice.ingest

