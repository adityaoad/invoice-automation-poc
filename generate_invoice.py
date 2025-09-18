from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

pdf.cell(200, 10, txt="Sample Invoice", ln=True, align='C')
pdf.cell(200, 10, txt="Invoice Number: INV-12345", ln=True)
pdf.cell(200, 10, txt="Date: 2025-07-31", ln=True)
pdf.cell(200, 10, txt="Vendor: Acme Corp", ln=True)
pdf.cell(200, 10, txt="Total: $1,234.56", ln=True)

pdf.output("sample_invoice.pdf")
print("Fake invoice generated!")
