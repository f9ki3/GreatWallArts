import json
import random
from datetime import datetime, timedelta

# Load the products data
file_path = "static/json/products.json"
with open(file_path, "r") as file:
    products = json.load(file)

# Define invoice parameters 
tax_rate = 10  # 10% tax rate
discount_rate = 5  # 5% discount

# Generate random invoices for February 2024
invoices = []
start_date = datetime(2024, 2, 1)
end_date = datetime(2024, 2, 28)

invoice_id = 1001  # Start invoice numbering

while start_date <= end_date:
    num_items = random.randint(1, 5)  # Number of items in a transaction
    selected_items = random.sample(products, num_items)  # Select random products

    cart_items = []
    subtotal = 0

    for item in selected_items:
        # Get prices, ensuring they are valid numbers
        sale_price = item.get("sale_price")
        regular_price = item.get("regular_price", 0)

        # Ensure sale_price is valid; otherwise, fallback to regular_price
        try:
            sale_price = float(sale_price) if sale_price is not None else float(regular_price)
        except ValueError:
            sale_price = float(regular_price)

        quantity = random.randint(1, 3)  # Random quantity per item
        total_price = sale_price * quantity  # No more 'NoneType' error

        cart_items.append({
            "name": item.get("name", "Unknown Product"),
            "brand": item.get("brand", "Unknown Brand"),
            "quantity": quantity,
            "unit_price": sale_price,
            "total_price": round(total_price, 2)
        })
        
        subtotal += total_price

    # Calculate tax, discount, and total amount
    tax_amount = round(subtotal * (tax_rate / 100), 2)
    discount_amount = round(subtotal * (discount_rate / 100), 2)
    total_amount = round(subtotal + tax_amount - discount_amount, 2)

    # Create invoice entry
    invoice = {
        "invoice": {
            "invoice_id": invoice_id,
            "invoice_number": f"INV-{start_date.strftime('%Y%m%d')}",
            "po_id": f"PO-{random.randint(1000, 9999)}",
            "vendor_id": f"V-{random.randint(1000, 9999)}",
            "due_date": (start_date + timedelta(days=15)).strftime("%Y-%m-%d"),
            "subtotal": round(subtotal, 2),
            "tax_rate": tax_rate,
            "tax_amount": tax_amount,
            "discount_amount": discount_amount,
            "total_amount": total_amount,
            "status": random.choice(["Paid", "Pending"]),
            "created_at": start_date.strftime("%Y-%m-%d"),
            "updated_at": start_date.strftime("%Y-%m-%d"),
            "deleted_at": None
        },
        "purchase_order": {
            "po_id": f"PO-{random.randint(1000, 9999)}",
            "order_date": start_date.strftime("%Y-%m-%d"),
            "shipment_date": (start_date + timedelta(days=3)).strftime("%Y-%m-%d"),
            "delivery_date": (start_date + timedelta(days=10)).strftime("%Y-%m-%d"),
            "supplier": "Great Wall Arts PH",
            "products": cart_items
        }
    }

    invoices.append(invoice)
    invoice_id += 1
    start_date += timedelta(days=1)

# Save the generated invoices to a JSON file
output_path = "static/generated/invoices.json"
with open(output_path, "w") as outfile:
    json.dump({"invoices": invoices}, outfile, indent=2)

# Provide the output path
print(f"Invoices saved to: {output_path}")