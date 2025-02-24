import firebase_admin
import json
from firebase_admin import credentials, db

# Initialize Firebase
cred = credentials.Certificate("finance-department-3f0ba-firebase-adminsdk-fbsvc-1a069acada.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://finance-department-3f0ba-default-rtdb.asia-southeast1.firebasedatabase.app/"
})

# Load JSON file
with open("sales.json", "r") as file:
    items = json.load(file)

# Reference to "items" collection in Firebase
items_ref = db.reference("sales")

# Push each product to Firebaseasfg
for item in items:
    items_ref.push(item)

print("items added successfully!")