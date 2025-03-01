import json
import random
from datetime import datetime, timedelta

# Load the products data
file_path = "static/json/products.json"
with open(file_path, "r") as file:
    products = json.load(file)

# Generate random invoices
invoices = []
invoice_ids = [1001, 1002]
po_ids = ["PO-5678", "PO-6789"]
status_choices = ["Paid", "Pending"]

def generate_invoice(invoice_id, po_id, status):
    selected_products = random.sample(products, 4)  # Select 4 random products
    order_date = datetime(2025, 2, 20) + timedelta(days=random.randint(0, 5))
    shipment_date = order_date + timedelta(days=5)
    delivery_date = shipment_date + timedelta(days=10)
    due_date = delivery_date + timedelta(days=5)
    
    purchase_order = {
        "po_id": po_id,
        "order_date": order_date.strftime("%Y-%m-%d"),
        "shipment_date": shipment_date.strftime("%Y-%m-%d"),
        "delivery_date": delivery_date.strftime("%Y-%m-%d"),
        "supplier": "Great Wall Arts PH",
        "products": []
    }
    
    subtotal = 0
    for product in selected_products:
        quantity = random.randint(1, 3)
        unit_price = product.get("sale_price", 0) or product.get("regular_price", 0)  # Ensure no None values

        total_price = quantity * unit_price  # No more TypeError
        subtotal += total_price

        purchase_order["products"].append({
            "name": product["name"],
            "quantity": quantity,
            "unit_price": unit_price,
            "total_price": total_price
        })

    
    tax_rate = random.choice([10, 12])
    tax_amount = round((subtotal * tax_rate) / 100, 2)
    discount_amount = random.choice([200, 300])
    total_amount = round(subtotal + tax_amount - discount_amount, 2)
    created_at = datetime(2025, 2, invoice_id - 1000).strftime("%Y-%m-%d")
    
    invoice = {
        "invoice_id": invoice_id,
        "invoice_number": f"INV-202402{invoice_id - 1000}",
        "po_id": po_id,
        "vendor_id": f"V-{random.randint(1000, 9999)}",
        "due_date": due_date.strftime("%Y-%m-%d"),
        "subtotal": subtotal,
        "tax_rate": tax_rate,
        "tax_amount": tax_amount,
        "discount_amount": discount_amount,
        "total_amount": total_amount,
        "status": status,
        "created_at": created_at,
        "updated_at": None if status == "Pending" else created_at,
        "deleted_at": None
    }
    
    return {"invoice": invoice, "purchase_order": purchase_order}

for i in range(2):
    invoices.append(generate_invoice(invoice_ids[i], po_ids[i], status_choices[i]))

# Save the generated invoices to a JSON file
output_path = "static/generated/invoices.json"
with open(output_path, "w") as outfile:
    json.dump({"invoices": invoices}, outfile, indent=2)

# Provide the output path
output_path
