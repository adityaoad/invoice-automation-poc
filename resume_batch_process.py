import os
import openai
import pytesseract
from pdf2image import convert_from_path
import json

# ✅ CONFIG
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
invoice_dir = "bulk_invoices"
output_file = "results_styled.jsonl"

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

# ✅ OCR function
def extract_text_from_pdf(pdf_path):
    images = convert_from_path(pdf_path)
    text = ""
    for img in images:
        text += pytesseract.image_to_string(img)
    return text

# ✅ GPT extraction
def extract_fields_with_gpt(text):
    prompt = f"""
Extract the following fields from the invoice text below:

- Invoice Number
- Date
- Vendor
- Total Amount

Respond in JSON format only.

Invoice Text:
\"\"\"
{text}
\"\"\"
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content

# ✅ Process remaining invoices
with open(output_file, "a") as f_out:
    for filename in os.listdir(invoice_dir):
        if filename.endswith(".pdf") and filename not in processed_files:
            filepath = os.path.join(invoice_dir, filename)
            print(f"📄 Processing: {filename}")
            try:
                text = extract_text_from_pdf(filepath)
                extracted = extract_fields_with_gpt(text)
                result = {
                    "file": filename,
                    "output": json.loads(extracted)
                }
                f_out.write(json.dumps(result) + "\n")
                print("✅ Success")
            except Exception as e:
                print(f"❌ Failed to process {filename}: {e}")
