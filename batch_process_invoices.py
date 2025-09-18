import os
import openai
import pytesseract
from pdf2image import convert_from_path
import json

# ✅ CONFIG
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
invoice_dir = "invoices_output"
output_file =  "results_styled.jsonl"

# ✅ OCR function
def extract_text_from_pdf(pdf_path):
    images = convert_from_path(pdf_path)
    text = ""
    for img in images:
        text += pytesseract.image_to_string(img)
    return text

# ✅ GPT function using updated SDK
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

# ✅ Main batch loop
with open(output_file, "w") as f_out:
    for filename in os.listdir(invoice_dir):
        if filename.endswith(".pdf"):
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
