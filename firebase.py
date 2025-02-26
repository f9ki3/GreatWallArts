import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase
cred = credentials.Certificate("account_key.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://finance-department-3f0ba-default-rtdb.asia-southeast1.firebasedatabase.app/"
})

# Reference to the "sales" collection
sales_ref = db.reference("sales")

# Fetch sales data
sales_data = sales_ref.get()

# Print the retrieved data
if sales_data:
    print("Sales Data Retrieved:")
    for key, value in sales_data.items():
        print(f"ID: {key}, Data: {value}")
else:
    print("No sales data found.")
