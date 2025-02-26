from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import requests
import firebase_admin
from firebase_admin import credentials, db
import os

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import requests
import firebase_admin
from firebase_admin import credentials, db
import os
import json


# cred = credentials.Certificate("account_key.json")
# Get the credentials from environment variable
firebase_credentials = os.getenv("FIREBASE_CREDENTIALS")

if firebase_credentials:
    # Parse JSON string from environment variable
    cred_dict = json.loads(firebase_credentials)
    cred = credentials.Certificate(cred_dict)
else:
    raise ValueError("FIREBASE_CREDENTIALS environment variable is not set or invalid.")

# Initialize Firebase Admin SDK
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://finance-department-3f0ba-default-rtdb.asia-southeast1.firebasedatabase.app/"
})

app = Flask(__name__)
app.secret_key = '#@jhkasjahs'  # Required for session management

@app.route('/')
def RouteLogin():
    if 'user' not in session:  # Check if user is logged in
        return render_template('pages/index.html')       
    return redirect(url_for('dashboard'))

@app.route('/sales')
def sales():
    if 'user' not in session:  # Check if user is logged in
        return redirect(url_for('RouteLogin'))  # Redirect to login if not logged in
    return render_template('pages/sales.html')  # Show dashboard if logged in

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:  # Check if user is logged in
        return redirect(url_for('RouteLogin'))  # Redirect to login if not logged in
    return render_template('pages/dashboard.html')  # Show dashboard if logged in

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('RouteLogin'))

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()  # Correct way to get JSON data
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400  # Handle missing data

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    url = 'https://admin.gwamerchandise.com/api/auth'

    # Send request to external authentication API
    try:
        response = requests.post(url, json={"email": email, "password": password})
        response_data = response.json()

        if response.status_code == 200 and 'user' in response_data:
            session['user'] = response_data['user']  # Save response to session

        return jsonify(response_data), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to reach authentication server", "details": str(e)}), 500
    

# How to use
# GET /api/get-sales
# GET /api/get-sales?sort_by=total_sum&order=asc | total_sum, earnings, or timestamp
# GET /api/get-sales?page=2&per_page=3 | 
# GET /api/get-sales?id=-OJqeBQaJZ1aAeeseDeR

@app.route('/api/get-sales', methods=['GET'])
def get_sales():
    # Reference to the "sales" collection
    sales_ref = db.reference("sales")
    
    # Fetch sales data
    sales_data = sales_ref.get()
    
    if not sales_data:
        return jsonify({"message": "No sales data found"}), 404
    
    # Convert dict to list for sorting
    sales_list = [{"id": key, **value} for key, value in sales_data.items()]

    # Search by ID
    sale_id = request.args.get("id")
    if sale_id:
        sale = next((s for s in sales_list if s["id"] == sale_id), None)
        if sale:
            return jsonify({"sale": sale})
        return jsonify({"error": "Sale ID not found"}), 404

    # Sorting logic
    sort_by = request.args.get("sort_by", "timestamp")  # Default sorting by timestamp
    order = request.args.get("order", "desc")  # Default order is descending

    # Allowed sorting fields
    allowed_sort_fields = {"total_sum", "earnings", "timestamp"}

    if sort_by not in allowed_sort_fields:
        return jsonify({"error": "Invalid sort field. Use 'total_sum', 'earnings', or 'timestamp'"}), 400

    sales_list.sort(key=lambda x: x[sort_by], reverse=(order == "desc"))

    # Pagination logic
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))  # Default 10 records per page

    total_records = len(sales_list)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_sales = sales_list[start:end]

    # Response structure
    return jsonify({
        "total_records": total_records,
        "page": page,
        "per_page": per_page,
        "total_pages": (total_records + per_page - 1) // per_page,
        "sales": paginated_sales
    })


    
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
