
import os
import random
from fpdf import FPDF
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()
output_dir = "invoices_output"
os.makedirs(output_dir, exist_ok=True)

currencies = ["USD", "CAD", "INR", "GBP", "EUR", "JPY"]
tax_codes = ["TX-001", "TX-002", "TX-A", "GST-5%", "VAT-20%", "HST"]
layout_variants = [
    "top_left_logo", "top_right_logo", "center_logo",
    "left_billing_block", "right_billing_block", "split_block",
    "highlighted_table", "boxed_total", "bottom_terms_left", "bottom_terms_right"
]

def generate_line_items():
    items = [
        ("LED Bulbs", 2.00, 100), ("Electrical Cables (per meter)", 1.00, 50),
        ("Circuit Breakers", 10.00, 25), ("Wall Sockets", 5.00, 10),
        ("Switch Panels", 12.50, 5), ("Conduit Pipes", 3.25, 40)
    ]
    selected = random.sample(items, k=random.randint(3, 6))
    return [(desc, price, qty, price * qty) for desc, price, qty in selected]

def draw_invoice(index):
    vendor_name = fake.company()
    invoice_number = f"INV-{100000 + index}"
    invoice_date = datetime.today().date()
    due_date = invoice_date + timedelta(days=random.randint(10, 30))
    customer_name = fake.name()
    customer_address = fake.address().replace("\n", ", ")
    account_name = fake.bs().title()
    account_manager = fake.name()
    account_number = str(random.randint(1000000000, 9999999999))
    currency = random.choice(currencies)
    tax_code = random.choice(tax_codes)
    po_number = f"PO-{random.randint(10000, 99999)}"
    layout = "_".join(random.sample(layout_variants, 3))

    items = generate_line_items()
    subtotal = sum([item[3] for item in items])
    tax = round(subtotal * 0.05, 2)
    total = round(subtotal + tax, 2)

    pdf = FPDF()
    pdf.add_page()

    if "top_left_logo" in layout:
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(100, 10, vendor_name, ln=0)
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 10, "[LOGO]", ln=1)
    elif "top_right_logo" in layout:
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, vendor_name, ln=1, align='R')
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 10, "[LOGO]", ln=1, align='R')
    else:
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, f"{vendor_name} | [LOGO]", ln=1, align='C')

    pdf.set_font("Arial", '', 11)
    pdf.ln(4)

    pdf.cell(0, 8, f"Invoice Number: {invoice_number}", ln=1)
    pdf.cell(0, 8, f"PO Number: {po_number}", ln=1)
    pdf.cell(0, 8, f"Invoice Date: {invoice_date}  |  Due Date: {due_date}", ln=1)
    pdf.cell(0, 8, f"Account Manager: {account_manager}", ln=1)
    pdf.cell(0, 8, f"Account Name: {account_name}", ln=1)
    pdf.cell(0, 8, f"Account Number: {account_number}", ln=1)
    pdf.cell(0, 8, f"Currency: {currency}  |  Tax Code: {tax_code}", ln=1)
    pdf.cell(0, 8, f"Customer: {customer_name}", ln=1)
    pdf.multi_cell(0, 8, f"Customer Address: {customer_address}")
    pdf.ln(5)

    # Table
    pdf.set_font("Arial", 'B', 11)
    pdf.set_fill_color(120, 120, 180) if "highlighted_table" in layout else pdf.set_fill_color(200)
    pdf.set_text_color(255 if "highlighted_table" in layout else 0)

    pdf.cell(30, 8, "QTY", 1, 0, 'C', 1)
    pdf.cell(90, 8, "DESCRIPTION", 1, 0, 'C', 1)
    pdf.cell(35, 8, "UNIT PRICE", 1, 0, 'C', 1)
    pdf.cell(35, 8, "AMOUNT", 1, 1, 'C', 1)

    pdf.set_font("Arial", '', 11)
    pdf.set_text_color(0)
    for desc, price, qty, amt in items:
        pdf.cell(30, 8, str(qty), 1)
        pdf.cell(90, 8, desc, 1)
        pdf.cell(35, 8, f"{currency} {price:.2f}", 1, 0, 'R')
        pdf.cell(35, 8, f"{currency} {amt:.2f}", 1, 1, 'R')

    pdf.cell(155, 8, "Subtotal", 1)
    pdf.cell(35, 8, f"{currency} {subtotal:.2f}", 1, 1, 'R')
    pdf.cell(155, 8, "Tax (5%)", 1)
    pdf.cell(35, 8, f"{currency} {tax:.2f}", 1, 1, 'R')
    pdf.cell(155, 8, "Total", 1)
    pdf.cell(35, 8, f"{currency} {total:.2f}", 1, 1, 'R')

    pdf.ln(6)
    if "bottom_terms_right" in layout:
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(0, 6, "Terms and Conditions", ln=1, align='R')
        pdf.set_font("Arial", '', 9)
        pdf.multi_cell(0, 6, "Payment is due in 14 days. Please make checks payable to the vendor.", align='R')
    else:
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(0, 6, "Terms and Conditions", ln=1)
        pdf.set_font("Arial", '', 9)
        pdf.multi_cell(0, 6, "Payment is due in 14 days. Please make checks payable to the vendor.")

    output_path = os.path.join(output_dir, f"styled_invoice_{index}.pdf")
    pdf.output(output_path)

if __name__ == "__main__":
    print("Generating 2000 styled invoices...")
    for i in range(2000):
        draw_invoice(i)
    print("Done! Invoices saved to ./invoices_output/")
