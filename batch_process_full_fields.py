
import os
import openai
import pytesseract
from pdf2image import convert_from_path
import json

# ✅ CONFIG
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
invoice_dir = "invoices_output"
output_file = "results_full_fields.jsonl"

# ✅ Load previously processed files
processed_files = set()
if os.path.exists(output_file):
    with open(output_file, "r") as f:
        for line in f:
            try:
                data = json.loads(line)
                processed_files.add(data.get("file"))
            except:
                continue

# ✅ OCR
def extract_text_from_pdf(pdf_path):
    images = convert_from_path(pdf_path)
    text = ""
    for img in images:
        text += pytesseract.image_to_string(img)
    return text

# ✅ GPT Extraction
def extract_all_fields_with_gpt(text):
    prompt = (
        "Extract the following fields from the invoice text below:\n\n"
        "- Invoice Number\n"
        "- Invoice Date\n"
        "- Due Date\n"
        "- Vendor Name\n"
        "- Vendor Address\n"
        "- PO Number\n"
        "- Billing Period\n"
        "- Account Number\n"
        "- Account Name\n"
        "- Account Manager\n"
        "- Tax Code\n"
        "- Tax Amount\n"
        "- Currency\n"
        "- Total Amount\n\n"
        "Respond in compact JSON format only.\n\n"
        f"Invoice Text:\n{text}"
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content

# ✅ Get list of unprocessed files
all_files = sorted([f for f in os.listdir(invoice_dir) if f.endswith(".pdf")])
unprocessed = [f for f in all_files if f not in processed_files]
total = len(unprocessed)

# ✅ Main Loop with counter
with open(output_file, "a") as f_out:
    for idx, filename in enumerate(unprocessed, start=1):
        filepath = os.path.join(invoice_dir, filename)
        print(f"📄 Processing: {filename} ({idx}/{total})")
        try:
            text = extract_text_from_pdf(filepath)
            extracted = extract_all_fields_with_gpt(text)
            result = {
                "file": filename,
                "output": json.loads(extracted)
            }
            f_out.write(json.dumps(result) + "\n")
            print("✅ Success")
        except Exception as e:
            print(f"❌ Failed to process {filename}: {e}")
