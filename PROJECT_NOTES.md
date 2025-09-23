Invoice Automation POC
Overview

This Proof of Concept automates vendor invoice processing. It ingests invoices received via email, extracts fields using OCR + GPT, and saves the results either in PostgreSQL or Excel (SharePoint/OneDrive).

The goal is to reduce manual Accounts Payable (AP) work and improve accuracy, speed, and auditability.

Workflow

Email ingestion

Emails (Gmail/Outlook via IMAP) with PDF attachments are fetched.

Attachments are downloaded into a staging folder.

OCR (Optical Character Recognition)

pdf2image converts PDFs → images.

pytesseract extracts raw text.

LLM-based field extraction

GPT (gpt-3.5-turbo) is prompted with invoice text.

Extracted fields: Invoice Number, Date, Due Date, Vendor, Address, PO, Billing Period, Tax, Currency, Amount, etc.

Storage
Two options implemented:

PostgreSQL (normalized schema)

Tables: vendors, accounts, purchase_orders, invoices, email_invoices.

Excel (for AP batch uploads)

Each invoice split into 2 rows: Item and Tax.

Fixed headers must exist in the Excel sheet.

Most columns use static placeholder values; only 4 columns (Invoice Number, Invoice Date, Type, Amount) are dynamic.

Notifications (optional)

Updated Excel files can be emailed via SMTP.

Folder / File Structure
Invoice Automation Project/
│
├── ingest_outlook_imap_to_postgres.py   # Main pipeline: IMAP → OCR → GPT → DB/Excel
├── batch_process_invoices.py            # Batch OCR + GPT for bulk PDFs
├── batch_process_full_fields.py         # Extended extraction (all fields)
├── extract_fields.py                    # Standalone GPT field extraction
├── insert_to_pgsql.py                   # DB insert helper
├── generate_realistic_invoices.py       # Creates fake test invoices
├── PROJECT_NOTES.md                     # This documentation
├── requirements.txt                     # Python dependencies
└── .env.example                         # Template for environment variables

Environment Setup

Clone repo

git clone https://github.com/adityaoad/invoice-automation-poc.git
cd invoice-automation-poc


Python environment (Windows/Mac)

python -m venv venv
source venv/bin/activate    # Mac/Linux
venv\Scripts\activate       # Windows


Install dependencies

pip install -r requirements.txt


Create .env from template

cp .env.example .env


Then update with your values.

.env Variables
# Gmail IMAP
GMAIL_EMAIL=your_email@gmail.com
GMAIL_APP_PASSWORD=your_app_password
IMAP_HOST=imap.gmail.com
IMAP_PORT=993
GMAIL_LABEL=Invoices   # Gmail label to check

# OpenAI
OPENAI_API_KEY=sk-...

# PostgreSQL
PG_DB=invoice_db
PG_USER=postgres
PG_PASSWORD=your_password
PG_HOST=localhost
PG_PORT=5432

# Excel / SharePoint
XLSX_PATH=/path/to/Invoice POC.xlsx

# SMTP for notifications (optional)
SMTP_EMAIL=your_email@gmail.com
SMTP_APP_PASSWORD=your_app_password
NOTIFY_EMAIL=recipient@company.com

Key Scripts

ingest_outlook_imap_to_postgres.py
Main pipeline. Ingests invoices from email → runs OCR + GPT → writes to DB and/or Excel.

generate_realistic_invoices.py
Generates test PDFs with randomized formatting and fields.

batch_process_full_fields.py
Processes a folder of PDFs, extracts all fields, saves as JSONL.

Important Notes

Excel headers must match exactly:

invoice number | invoice date | supplier number | supplier site | description | pay group | today's date | type | amount | line description | entity | region | function | expense account | product | project | intercompany | future use | N/A


Only 4 columns are dynamic: Invoice Number, Invoice Date, Type, Amount.

Every invoice → 2 rows (Item + Tax).

All other columns are fixed placeholders (Fixed Value) unless business logic overrides them.

OneDrive sync can delay updates — local paths are faster for testing.

Performance

Processing time: ~5–7 sec per invoice (OCR + GPT + write).

Cost: $0.001–$0.003 per invoice (depends on token size and model).

Handles up to ~2000 invoices/month (current scope).

AI/ML Context

OCR is Computer Vision.

GPT is a pre-trained LLM used for Information Extraction (not fine-tuned).

Feedback loop can be added (store failed parses → re-prompt or retrain).
