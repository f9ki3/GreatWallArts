import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate("account_key.json")
# cred = credentials.Certificate("/etc/secrets/account_key.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://finance-department-3f0ba-default-rtdb.asia-southeast1.firebasedatabase.app/"
})
# Get Firestore database reference
db = firestore.client()

# Collection and document reference
collection_name = "budget_limit"
doc_id = "default"  # Document ID (you can change it)

# Check if the document already exists
doc_ref = db.collection(collection_name).document(doc_id)
doc = doc_ref.get()

if doc.exists:
    print(f"Document '{doc_id}' already exists with data:", doc.to_dict())
else:
    # Insert data
    doc_ref.set({"budget_limit": 50000})
    print(f"Collection '{collection_name}' created with budget_limit = 50000.")
