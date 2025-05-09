import firebase_admin
import json
from firebase_admin import credentials, db

# Initialize Firebase Admin SDK
cred = credentials.Certificate("account_key.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://finance-department-3f0ba-default-rtdb.asia-southeast1.firebasedatabase.app/"
})

# Load JSON data from file
with open("static/json/logistics.json", "r") as file:
    data = json.load(file)

# Reference to "general_ledger" collection
ledger_ref = db.reference("logistics")

# Push each item to Firebase
for item in data:
    ledger_ref.push(item)

print("Items added successfully!")



# import firebase_admin
# from firebase_admin import credentials, db
# from datetime import datetime

# # Initialize Firebase
# cred = credentials.Certificate("account_key.json")
# firebase_admin.initialize_app(cred, {
#     "databaseURL": "https://finance-department-3f0ba-default-rtdb.asia-southeast1.firebasedatabase.app/"
# })

# # Reference to the "reports" collection (node)
# reports_ref = db.reference("reports")

# # Sample data to add
# report_data = {
#     "report_number": "RPT-1001",
#     "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#     "type": "Financial Report",
#     "start_date": "2025-03-01",
#     "end_date": "2025-03-07",
#     "link": "https://example.com/report.pdf"
# }

# # Push new report data
# new_report_ref = reports_ref.push(report_data)

# print(f"New report added with key: {new_report_ref.key}")
