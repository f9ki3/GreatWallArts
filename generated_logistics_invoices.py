import json
import random
from datetime import datetime, timedelta

def load_products(filename="static/json/products.json"):
    """ Load products from a JSON file. """
    with open(filename, "r") as file:
        data = json.load(file)
    
    if isinstance(data, dict) and "products" in data:
        return data["products"]
    elif isinstance(data, list):
        return data
    else:
        raise ValueError("Invalid JSON format for products.")

def generate_invoice_id(index):
    """ Generate a unique invoice ID. """
    return 1000 + index

def generate_invoice_number(date):
    """ Generate an invoice number based on the date. """
    return f"INV-{date.strftime('%Y%m%d')}"

def generate_po_id(index):
    """ Generate a unique purchase order ID. """
    return f"PO-{5000 + index}"

def generate_due_date(invoice_date):
    """ Generate a due date, 30 days after the invoice date. """
    return (invoice_date + timedelta(days=30)).strftime("%Y-%m-%d")

def generate_invoice(date, index, products):
    """ Generate a single invoice with random valid products. """
    # ✅ Exclude products with sale_price of 0 or None
    valid_products = [p for p in products if isinstance(p.get("sale_price"), (int, float)) and p["sale_price"] > 0]

    if len(valid_products) < 2:
        return None  # Skip invoice if there aren't enough valid products

    selected_products = random.sample(valid_products, random.randint(2, min(5, len(valid_products))))

    for product in selected_products:
        product["quantity"] = random.randint(1, 5)
        product["total_price"] = product["quantity"] * product["sale_price"]

    subtotal = sum(p["total_price"] for p in selected_products)
    tax_rate = random.choice([5, 10, 12, 15])
    tax_amount = subtotal * (tax_rate / 100)
    discount_amount = random.choice([0, 100, 200, 300])
    total_amount = subtotal + tax_amount - discount_amount
    status = random.choice(["Paid", "Pending", "Overdue"])
    
    invoice_id = generate_invoice_id(index)
    invoice_number = generate_invoice_number(date)
    po_id = generate_po_id(index)
    vendor_id = f"V-{random.randint(1000, 9999)}"
    due_date = generate_due_date(date)
    created_at = date.strftime("%Y-%m-%d")

    return {
        "invoice": {
            "invoice_id": invoice_id,
            "invoice_number": invoice_number,
            "po_id": po_id,
            "vendor_id": vendor_id,
            "due_date": due_date,
            "subtotal": round(subtotal, 2),
            "tax_rate": tax_rate,
            "tax_amount": round(tax_amount, 2),
            "discount_amount": discount_amount,
            "total_amount": round(total_amount, 2),
            "status": status,
            "created_at": created_at,
            "updated_at": created_at,
            "deleted_at": None
        },
        "purchase_order": {
            "po_id": po_id,
            "order_date": created_at,
            "shipment_date": (date + timedelta(days=5)).strftime("%Y-%m-%d"),
            "delivery_date": (date + timedelta(days=10)).strftime("%Y-%m-%d"),
            "supplier": "Great Wall Arts PH",
            "products": selected_products
        }
    }

def generate_invoices():
    """ Generate invoices for every day from Jan 1 to Dec 31, 2024. """
    products = load_products()
    invoices = []
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 31)
    days = (end_date - start_date).days + 1  # 366 days (leap year)

    for i in range(days):
        invoice_date = start_date + timedelta(days=i)
        invoice = generate_invoice(invoice_date, i + 1, products)
        if invoice:  # ✅ Only add valid invoices
            invoices.append(invoice)

    with open("generated_invoices.json", "w") as file:
        json.dump({"invoices": invoices}, file, indent=4)

if __name__ == "__main__":
    generate_invoices()
    print("✅ Invoices generated for all 366 days of 2024 and saved to generated_invoices.json")
