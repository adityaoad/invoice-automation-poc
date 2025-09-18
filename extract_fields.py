import openai

# ✅ Paste your real API key here
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ✅ This is the OCR'd invoice text
invoice_text = """
Sample Invoice
Invoice Number: INV-12345
Date: 2025-07-31
Vendor: Acme Corp
Total: $1,234.56
"""

# ✅ The prompt we'll send to GPT-3.5
prompt = f"""
Extract the following fields from the invoice text below:

- Invoice Number
- Date
- Vendor
- Total Amount

Respond only in JSON format.

Invoice Text:
\"\"\"
{invoice_text}
\"\"\"
"""

# ✅ GPT-3.5 request
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": prompt}
    ],
    temperature=0
)

# ✅ Print the response
print(response.choices[0].message.content)
