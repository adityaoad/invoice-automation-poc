import json
import psycopg2

# ✅ Config
jsonl_file = "results_full_fields.jsonl"

conn = psycopg2.connect(
    dbname="invoice_db",
    user="postgres",
    password="saroj@227",  # replace with your actual password
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# ✅ Helper cache to avoid duplicate inserts
vendor_cache = {}
account_cache = {}
po_cache = {}

def get_or_create(table, unique_key, data_dict):
    """
    Insert into table if unique_key not already cached.
    Return the ID from cache or after insert.
    """
    cache = {
        "vendors": vendor_cache,
        "accounts": account_cache,
        "purchase_orders": po_cache
    }[table]

    key = data_dict[unique_key]
    if key in cache:
        return cache[key]

    # Insert and get ID
    cols = ", ".join(data_dict.keys())
    placeholders = ", ".join(["%s"] * len(data_dict))
    values = list(data_dict.values())
    insert_sql = f"INSERT INTO invoice_ai.{table} ({cols}) VALUES ({placeholders}) RETURNING id"
    cursor.execute(insert_sql, values)
    id = cursor.fetchone()[0]
    conn.commit()
    cache[key] = id
    return id

# ✅ Load and insert
with open(jsonl_file, "r") as f:
    for line in f:
        entry = json.loads(line)
        file = entry.get("file")
        output = entry.get("output", {})

        # 1. Normalize vendor
        vendor_id = get_or_create("vendors", "name", {
            "name": output.get("Vendor Name"),
            "address": output.get("Vendor Address", "")
        })

        # 2. Normalize account
        account_id = get_or_create("accounts", "number", {
            "number": output.get("Account Number", ""),
            "name": output.get("Account Name", ""),
            "manager": output.get("Account Manager", "")
        })

        # 3. Normalize PO
        po_id = get_or_create("purchase_orders", "po_number", {
            "po_number": output.get("PO Number", ""),
            "billing_period": output.get("Billing Period", ""),
            "tax_code": output.get("Tax Code", ""),
            "tax_amount": output.get("Tax Amount", "")
        })

        # 4. Insert invoice
        invoice_sql = """
        INSERT INTO invoice_ai.invoices (
            file, invoice_number, invoice_date, due_date, currency, total_amount,
            vendor_id, account_id, po_id
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (file) DO NOTHING
        """
        invoice_data = (
            file,
            output.get("Invoice Number"),
            output.get("Invoice Date"),
            output.get("Due Date"),
            output.get("Currency"),
            output.get("Total Amount"),
            vendor_id,
            account_id,
            po_id
        )
        cursor.execute(invoice_sql, invoice_data)
        conn.commit()

print("✅ Done inserting normalized data.")
cursor.close()
conn.close()
