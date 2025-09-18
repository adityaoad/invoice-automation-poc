import psycopg2
import json

# ✅ PostgreSQL connection
conn = psycopg2.connect(
    dbname="invoice_db",
    user="postgres",
    password="saroj@227", 
    host="localhost",
    port="5432"
)

cur = conn.cursor()

# ✅ Read JSONL results
with open("results.jsonl") as f:
    for line in f:
        record = json.loads(line)
        file_name = record["file"]
        output = record["output"]

        try:
            cur.execute("""
                INSERT INTO vendor_invoices (file_name, invoice_number, invoice_date, vendor, total_amount)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                file_name,
                output["Invoice Number"],
                output["Date"],
                output["Vendor"],
                float(output["Total Amount"].replace("$", "").replace(",", ""))
            ))
        except Exception as e:
            print(f"❌ Failed to insert {file_name}: {e}")

# ✅ Commit and close
conn.commit()
cur.close()
conn.close()

print("✅ All records inserted into PostgreSQL.")
