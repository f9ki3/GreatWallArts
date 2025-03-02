from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import requests
import firebase_admin
from datetime import datetime
from firebase_admin import credentials, db

# Initialize Firebase
# cred = credentials.Certificate("account_key.json")
cred = credentials.Certificate("/etc/secrets/account_key.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://finance-department-3f0ba-default-rtdb.asia-southeast1.firebasedatabase.app/"
})

app = Flask(__name__)
app.secret_key = '#@jhkasjahs'  # Required for session management

# Custom 404 error handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template('/pages/404.html'), 404

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

@app.route('/publish_job')
def publish_job():
    if 'user' not in session:  # Check if user is logged in
        return redirect(url_for('RouteLogin'))  # Redirect to login if not logged in
    return render_template('pages/publish_job.html')  # Show dashboard if logged in


@app.route('/documentation')
def documentation():
    return render_template('pages/documentation.html')  # Show dashboard if logged in

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:  # Check if user is logged in
        return redirect(url_for('RouteLogin'))  # Redirect to login if not logged in
    return render_template('pages/dashboard.html')  # Show dashboard if logged in

@app.route('/view_sales')
def view_sales():
    if 'user' not in session:  # Check if user is logged in
        return redirect(url_for('RouteLogin'))  # Redirect to login if not logged in
    return render_template('pages/view_sales.html')  # Show dashboard if logged in

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


@app.route('/api/generate-sales', methods=['POST'])
def generate_sales():

    # Get sales data from request body
    sales_data = request.json  

    if not sales_data:
        return jsonify({
            "status": "error",
            "message": "Invalid or missing sales data."
        }), 400

    # Reference to the "sales" collection
    sales_ref = db.reference("sales")

    # Save data to Firebase with a unique key
    new_sale_ref = sales_ref.push(sales_data)

    return jsonify({
        "status": "success",
        "message": "Sales invoice generated successfully.",
        "sale_id": new_sale_ref.key  # Return generated key for reference
    })

@app.route('/api/delete-sale/<sale_id>', methods=['DELETE'])
def delete_sale(sale_id):
    """Deletes a specific sale entry from Firebase using its unique key."""

    # Reference to the specific sale entry
    sale_ref = db.reference(f"sales/{sale_id}")

    # Check if the sale exists
    if not sale_ref.get():
        return jsonify({
            "status": "error",
            "message": "Sale ID not found."
        }), 404

    # Delete the sale entry
    sale_ref.delete()

    return jsonify({
        "status": "success",
        "message": f"Sale with ID {sale_id} has been deleted."
    })

# How to use
# GET /api/get-logistics
# GET /api/get-logistics?start_date=2024-01-01&end_date=2024-01-31
# GET /api/get-logistics?sort=desc
# GET /api/get-logistics?invoice_id=1001
# GET /api/get-logistics?page=2&per_page=10

@app.route('/api/get-logistics', methods=['GET'])
def get_logistics():
    logistics_ref = db.reference("logistics")
    logistics_data = logistics_ref.get()

    if not logistics_data:
        return jsonify({"message": "No logistics data found"}), 404

    # Convert dictionary to list for sorting, pagination, and searching
    logistics_list = list(logistics_data.values())

    # Get query parameters
    invoice_id = request.args.get('invoice_id')
    sort_order = request.args.get('sort', 'asc')  # Default to ascending
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)  # Default 5 per page

    # Search by invoice_id
    if invoice_id:
        logistics_list = [item for item in logistics_list if str(item['invoice']['invoice_id']) == invoice_id]

    # Sort data by invoice_id
    logistics_list.sort(key=lambda x: x['invoice']['invoice_id'], reverse=(sort_order == 'desc'))

    # Pagination
    total_items = len(logistics_list)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_data = logistics_list[start:end]

    return jsonify({
        "total_items": total_items,
        "page": page,
        "per_page": per_page,
        "total_pages": (total_items + per_page - 1) // per_page,  # Compute total pages
        "data": paginated_data
    }), 200

@app.route('/api/get-logistics-reports', methods=['GET'])
def get_logistics_reports():
    logistics_ref = db.reference("logistics")
    logistics_data = logistics_ref.get()

    if not logistics_data:
        return jsonify({"message": "No logistics data found"}), 404

    # Convert dictionary to list
    logistics_list = list(logistics_data.values())

    # Get query parameters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if not start_date or not end_date:
        return jsonify({"error": "Missing required parameters: start_date and end_date"}), 400

    try:
        start_dt = datetime.strptime(start_date.strip(), "%Y-%m-%d")
        end_dt = datetime.strptime(end_date.strip(), "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    if start_dt > end_dt:
        return jsonify({"error": "start_date cannot be greater than end_date"}), 400

    # Filter invoices by date range
    filtered_logistics = []
    for item in logistics_list:
        invoice = item.get('invoice', {})
        created_at = invoice.get('created_at')
        if created_at:
            try:
                invoice_date = datetime.strptime(created_at, "%Y-%m-%d")
                if start_dt <= invoice_date <= end_dt:
                    filtered_logistics.append(item)
            except ValueError:
                continue  # Skip records with invalid dates

    if not filtered_logistics:
        return jsonify({"message": "No logistics data found for the given date range."}), 404

    # Generate summary
    total_invoices = len(filtered_logistics)
    total_amount = sum(float(item.get('invoice', {}).get('total_amount', 0)) for item in filtered_logistics)

    status_counts = {}
    for item in filtered_logistics:
        status = item.get('invoice', {}).get('status', 'Unknown')  # Fix the status extraction
        status_counts[status] = status_counts.get(status, 0) + 1


    summary_report = {
        "start_date": start_date,
        "end_date": end_date,
        "total_invoices": total_invoices,
        "total_amount": total_amount,
        "status_summary": status_counts
    }

    return jsonify({
        "summary_report": summary_report,
        "invoices": filtered_logistics
    }), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
