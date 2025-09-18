from pdf2image import convert_from_path
import pytesseract

pdf_path = "sample_invoice.pdf"
images = convert_from_path(pdf_path)

for i, img in enumerate(images):
    text = pytesseract.image_to_string(img)
    print(f"\n--- Page {i + 1} ---\n")
    print(text)
