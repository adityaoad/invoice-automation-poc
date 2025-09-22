# Invoice Automation PoC – Full Project Notes

## 📌 Project Purpose
This Proof of Concept (PoC) automates the **end-to-end invoice processing pipeline**.  
The goal is to eliminate manual data entry by:
1. Ingesting invoices directly from email (Gmail or Outlook IMAP).
2. Extracting all important fields from attached PDFs using **OCR + AI**.
3. Splitting costs into line items (Item + Tax).
4. Writing structured data into either:
   - a **Postgres normalized schema** (for structured queries), OR  
   - a **SharePoint/OneDrive Excel template** (for direct AP upload).

This is a hybrid **process + tool**:  
- Process = Email → OCR → AI → Post-processing → Output.  
- Tool = Python scripts that automate each step.

---

## 🛠 Tech Stack
- **Python 3.9+**
- **OCR & PDF tools**
  - [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
  - [Poppler](https://poppler.freedesktop.org/) (for PDF → images)
- **AI**
  - [OpenAI GPT-3.5](https://platform.openai.com/docs/) for field extraction
- **Database**
  - PostgreSQL (normalized schema: vendors, accounts, purchase orders, invoices, email_invoices)
- **File Output**
  - Excel via [openpyxl](https://openpyxl.readthedocs.io/en/stable/)  
  - Supports writing to SharePoint/OneDrive synced paths
- **Email Intake**
  - [imapclient](https://imapclient.readthedocs.io/en/2.3.1/) for IMAP
- **Secrets**
  - Managed via `.env` file (ignored by Git, template provided in `.env.example`)

---

## 📂 Key Files
- **`ingest_outlook_imap_to_postgres.py`**  
  Main pipeline: connects to IMAP, downloads invoice PDFs, OCR + GPT extraction, inserts into Postgres or appends to Excel.
- **`batch_process_full_fields.py`**  
  Batch processor for local PDFs (used for 2000+ fake invoice test set).
- **`generate_realistic_invoices.py`**  
  Generates fake invoices with realistic structure, random vendor layouts, logos, tax splits, etc.
- **`PROJECT_NOTES.md`** (this file)  
  Documentation for setup, flow, and design decisions.
- **`.env.example`**  
  Template for secrets/config.

### Old/optional files (can be deleted in production):
- `extract_fields.py` (early GPT test)
- `ocr_test.py` (basic OCR test)
- `resume_batch_process.py` (retry utility, not needed anymore)

---

## 🔑 Environment Variables
Defined in `.env` (local only).  
Template `.env.example` is versioned in GitHub.

| Variable | Purpose |
|----------|---------|
| OPENAI_API_KEY | Your OpenAI API key |
| GMAIL_EMAIL | Gmail address for invoice intake |
| GMAIL_APP_PASSWORD | Gmail app password (16 chars, generated in Google security settings) |
| IMAP_HOST | IMAP server (e.g. `imap.gmail.com`) |
| IMAP_PORT | `993` |
| GMAIL_LABEL | Gmail label to scan for invoices (e.g. `Invoices`) |
| SHAREPOINT_XLSX | Full path to Excel file (local or OneDrive synced) |
| PG_DB, PG_USER, PG_PASSWORD, PG_HOST, PG_PORT | Postgres connection info |

---

## 🔄 Workflow: End-to-End Flow

```text
📥 Email Intake
   ↓
📄 PDF Extraction
   - Save attachments to inbox_downloads/
   - OCR with Tesseract + Poppler
   ↓
🧠 AI Field Extraction
   - LLM parses text into JSON fields
   - Fields: Invoice No, Date, Due Date, Vendor, Address, PO, Account, Tax, Currency, Total
   ↓
✅ Post-Processing
   - Normalize dates (handles YYYY-MM-DD, MM-DD-YYYY, DD-MM-YYYY)
   - Split into 2 rows: ITEM + TAX
   - Fill fixed values for AP fields
   ↓
📊 Output
   - Option A: Insert into Postgres (normalized schema)
   - Option B: Append 2 rows to Excel file (SharePoint/OneDrive)
   ↓
📧 Notification (optional)
   - Email updated Excel to AP team
🗃 Database Schema (Postgres Option)
Schema: invoice_ai

Tables:

vendors (id, name, address)

accounts (id, number, name, manager)

purchase_orders (id, po_number, billing_period, tax_code, tax_amount)

invoices (id, file, invoice_number, invoice_date, due_date, currency, total_amount, vendor_id, account_id, po_id)

email_invoices (id, message_id, subject, sender, received_at, file_name)

📊 Excel Output (SharePoint Option)
Excel columns:

invoice number

invoice date

supplier number

supplier site

description

pay group

today’s date

type (ITEM / TAX)

amount

line description

entity

region

function

expense account

product

project

intercompany

future use

N/A

Logic:

Only 4 dynamic columns are filled from GPT extraction:

invoice number

invoice date

type

amount

All other columns are filled with "Fixed Value" (for now).

ITEM row = total minus tax.

TAX row = tax amount.

🪟 Windows-Specific Notes
Install Tesseract: C:\Program Files\Tesseract-OCR\tesseract.exe

Install Poppler: e.g., C:\poppler\Library\bin

Update code:

python
Copy code
import platform
if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    POPPLER_PATH = r"C:\poppler\Library\bin"
else:
    POPPLER_PATH = None
images = convert_from_path(pdf_path, poppler_path=POPPLER_PATH)
.env Excel path example:

ini
Copy code
SHAREPOINT_XLSX=C:\Users\<user>\OneDrive - Company\AP\Invoice POC.xlsx
📈 Performance & Cost
2000 invoices processed in batch test.

Processing time: ~3–5 seconds per invoice.

OpenAI cost (GPT-3.5): <$10 for 2000 invoices.

Runs fine on a laptop.

✅ Current Status
Bulk pipeline verified (2000 fake invoices).

Gmail intake pipeline verified with live test.

Excel append logic verified.

Postgres integration tested.

OneDrive sync tested (works when file path points to local synced folder).

🚀 Next Steps
Add monitoring/metrics (success count, failures, processing time).

Add retry logic (for OCR/LLM/network issues).

Move cost center mapping logic to Snowflake (replace Winbill).

Package as a scheduled service (cron/Windows Task Scheduler).

(Optional) Add human-in-the-loop review for low-confidence extractions.

pgsql
Copy code

---

This way Copilot (and your VP deck) sees the **big picture**, step-by-step pipeline, schema, Excel format, Windows adjustments, costs, and next steps.  
