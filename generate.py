import json
import random
from datetime import datetime, timedelta

# Load the products data
file_path = "products.json"
with open(file_path, "r") as file:
    products = json.load(file)

# Generate random sales data for February 2024
# Regenerate sales data including regular_price in cart_items

sales_data = []
start_date = datetime(2024, 12, 1)
end_date = datetime(2024, 12, 31)

while start_date <= end_date:
    num_items = random.randint(1, 5)  # Number of items in a transaction
    selected_items = random.sample(products, num_items)  # Select random products

    cart_items = []
    total_sum = 0
    total_earnings = 0

    for item in selected_items:
        sale_price = item.get("sale_price", item.get("regular_price", 0))
        regular_price = item.get("regular_price", 0)
        if sale_price is not None:
            cart_items.append({
                "product_name": item["name"],
                "regular_price": regular_price,
                "sale_price": sale_price
            })
            total_sum += sale_price
            total_earnings += (regular_price - sale_price)

    timestamp = start_date.strftime("%Y-%m-%d %H:%M:%S")
    sales_data.append({
        "timestamp": timestamp,
        "cart_items": cart_items,
        "total_sum": round(total_sum, 2),
        "earnings": round(total_earnings, 2)
    })

    # Move to the next day
    start_date += timedelta(days=1)

# Save the updated sales data to a JSON file
output_path = "sales_results.json"
with open(output_path, "w") as outfile:
    json.dump(sales_data, outfile, indent=2)

# Provide the output path
output_path
