from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import requests
import firebase_admin
from firebase_admin import credentials, db, firestore
from datetime import datetime  # Ensure correct datetime import
import uuid


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

@app.route('/general_ledger')
def general_ledger():
    if 'user' not in session:  # Check if user is logged in
        return redirect(url_for('RouteLogin'))  # Redirect to login if not logged in
    return render_template('pages/general_ledger.html')  # Show dashboard if logged in

@app.route('/budget')
def budget():
    if 'user' not in session:  # Check if user is logged in
        return redirect(url_for('RouteLogin'))  # Redirect to login if not logged in
    return render_template('pages/budget.html')  # Show dashboard if logged in

@app.route('/logistics')
def logistics():
    if 'user' not in session:  # Check if user is logged in
        return redirect(url_for('RouteLogin'))  # Redirect to login if not logged in
    return render_template('pages/logistics.html')  # Show dashboard if logged in

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

@app.route('/create_budget')
def create_budget():
    if 'user' not in session:  # Check if user is logged in
        return redirect(url_for('RouteLogin'))  # Redirect to login if not logged in
    return render_template('pages/create_budget.html')  # Show dashboard if logged in

@app.route('/view_sales')
def view_sales():
    if 'user' not in session:  # Check if user is logged in
        return redirect(url_for('RouteLogin'))  # Redirect to login if not logged in
    return render_template('pages/view_sales.html')  # Show dashboard if logged in


@app.route('/view_request')
def view_request():
    if 'user' not in session:  # Check if user is logged in
        return redirect(url_for('RouteLogin'))  # Redirect to login if not logged in
    return render_template('pages/view_request.html')  # Show dashboard if logged in

@app.route('/view_logistics')
def view_logistics():
    if 'user' not in session:  # Check if user is logged in
        return redirect(url_for('RouteLogin'))  # Redirect to login if not logged in
    return render_template('pages/view_logistics.html')  # Show dashboard if logged in

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

@app.route('/api/sales-reports', methods=['GET'])
def get_sales_reports():
    # Reference to the "sales" collection
    sales_ref = db.reference("sales")
    
    # Fetch sales data
    sales_data = sales_ref.get()
    
    if not sales_data:
        return jsonify({"message": "No sales data found"}), 404
    
    # Convert dict to list for filtering
    sales_list = [{"id": key, **value} for key, value in sales_data.items()]
    
    # Date filtering
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    
    if start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400
        
        sales_list = [sale for sale in sales_list if start_date.date() <= datetime.strptime(sale["timestamp"], "%Y-%m-%d %H:%M:%S").date() <= end_date.date()]
    
    # Summary report calculation
    total_sales_amount = sum(sale.get("total_sum", 0) for sale in sales_list)
    total_sales_earnings = sum(sale.get("earnings", 0) for sale in sales_list)
    total_invoices = len(sales_list)
    
    summary_report = {
        "start_date": start_date.strftime("%Y-%m-%d") if start_date else None,
        "end_date": end_date.strftime("%Y-%m-%d") if end_date else None,
        "total_sales_amount": total_sales_amount,
        "total_sales_earnings": total_sales_earnings,
        "total_invoices": total_invoices
    }
    
    # Response structure
    return jsonify({
        "summary_report": summary_report,
        "sales invoices": sales_list
    })

#POST api/generate-sales
# {
#                 "timestamp": "2024-01-01 00:00:00",
#                 "cart_items": [
#                     {
#                         "product_name": "ABRAHAM 2024 PLANNER WITH MAGNETIC LOCK",
#                         "regular_price": 500.0,
#                         "sale_price": 399.0
#                     },
#                     {
#                         "product_name": "ELISHA 2 (CHEESEBOARD and WINE SET)",
#                         "regular_price": 1299.0,
#                         "sale_price": 999.0
#                     }
#                 ],
#                 "total_sum": 1398.0,
#                 "earnings": 401.0
#             }
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

    # Search by invoice_number, vendor_id, or po_id
    if invoice_id:
        logistics_list = [
            item for item in logistics_list 
            if str(item['invoice']['invoice_number']) == invoice_id
            or str(item['invoice']['vendor_id']) == invoice_id
            or str(item['invoice']['po_id']) == invoice_id
        ]


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

# api/get-logistics-reports?start_date=2024-01-01&end_date=2024-01-31
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
        "logistics invoices": filtered_logistics
    }), 200

@app.route('/api/get-budget', methods=['GET'])
def get_budget():
    # Get query parameters
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    reference_number = request.args.get('reference_number', default=None, type=str)
    sort_by = request.args.get('sort_by', default="date_of_request", type=str)
    order = request.args.get('order', default="desc", type=str).lower()

    # Reference to "budget" collection in Firebase
    budget_ref = db.reference("budget")
    budget_data = budget_ref.get()

    if not budget_data:
        return jsonify({"message": "No budget data found", "data": []}), 200

    # Convert dictionary to list of budget records
    budget_list = list(budget_data.values())

    # If searching by reference_number
    if reference_number:
        filtered_data = [item for item in budget_list if item.get("reference_number") == reference_number]
        return jsonify({
            "search": reference_number,
            "total_items": len(filtered_data),
            "data": filtered_data
        })

    # Sort the data
    valid_sort_fields = ["reference_number", "requested_by", "date_of_request", "department", "email", "status"]
    if sort_by in valid_sort_fields:
        budget_list = sorted(budget_list, key=lambda x: x.get(sort_by, ""), reverse=(order == "desc"))

    # Pagination logic
    total_items = len(budget_list)
    total_pages = (total_items + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    paginated_data = budget_list[start:end]

    return jsonify({
        "page": page,
        "per_page": per_page,
        "total_items": total_items,
        "total_pages": total_pages,
        "sort_by": sort_by,
        "order": order,
        "data": paginated_data
    })


# POST /api/request-budget
# {
#     "requested_by": "Juan Dela Cruz",
#     "department": "IT",
#     "email": "juan@example.com",
#     "contact": "+639123456789",
#     "budget_details": [
#         {
#             "amount": 1500,
#             "category": "Software",
#             "description": "Purchase of project management tool"
#         },
#         {
#             "amount": 3000,
#             "category": "Equipment",
#             "description": "New workstation setup"
#         }
#     ]
# }
@app.route('/api/request-budget', methods=['POST'])
def add_budget():
    try:
        # Parse JSON request body
        data = request.get_json()

        # Validate required fields
        required_fields = ["requested_by", "department", "email", "contact", "budget_details"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"'{field}' is required"}), 400

        # Generate a unique reference number
        reference_number = "REF" + str(uuid.uuid4().int)[:8]  # Generates a unique 8-digit reference

        # Set current date as the date_of_request
        date_of_request = datetime.now().strftime("%Y-%m-%d")  # ✅ Use datetime.now() instead

        # Construct budget entry
        budget_entry = {
            "requested_by": data["requested_by"],
            "department": data["department"],
            "email": data["email"],
            "contact": data["contact"],
            "date_of_request": date_of_request,
            "reference_number": reference_number,
            "status": "pending",  # Default status
            "budget_details": data["budget_details"]  # List of budget items
        }

        # Save to Firebase (generate unique key)
        budget_ref = db.reference("budget")
        new_budget = budget_ref.push(budget_entry)

        return jsonify({
            "message": "Budget request added successfully",
            "id": new_budget.key,
            "reference_number": reference_number
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/update-and-approve-budget', methods=['POST'])
def update_and_approve_budget():
    # Parse JSON request body
    data = request.get_json()
    reference_number = data.get('reference_number')

    if not reference_number:
        return jsonify({'error': 'Missing reference_number'}), 400

    # Reference the budget collection in Firebase
    budget_ref = db.reference('budget')
    budget_data = budget_ref.get()

    if not budget_data:
        return jsonify({'error': 'No budget records found'}), 404

    # Find the budget entry with the given reference_number
    matching_key = None
    matching_budget = None

    for key, budget in budget_data.items():
        if budget.get('reference_number') == reference_number:
            matching_key = key
            matching_budget = budget
            break

    if not matching_budget:
        return jsonify({'error': 'Budget entry not found'}), 404

    # Update the status to "approved"
    budget_ref.child(matching_key).update({'status': 'approved'})

    return jsonify({
        'message': 'Budget approved successfully',
        'reference_number': reference_number,
        'updated_budget': {**matching_budget, 'status': 'approved'}
    }), 200
    
@app.route('/api/delete-budget/<string:reference_number>', methods=['DELETE'])
def delete_budget(reference_number):
    if not reference_number:
        return jsonify({'error': 'Missing reference_number'}), 400

    # Reference the budget collection in Firebase
    budget_ref = db.reference('budget')
    budget_data = budget_ref.get()

    if not budget_data:
        return jsonify({'error': 'No budget records found'}), 404

    # Find the budget entry with the given reference_number
    matching_key = None

    for key, budget in budget_data.items():
        if budget.get('reference_number') == reference_number:
            matching_key = key
            break

    if not matching_key:
        return jsonify({'error': 'Budget entry not found'}), 404

    # Delete the budget entry
    budget_ref.child(matching_key).delete()

    return jsonify({
        'message': 'Budget entry deleted successfully',
        'reference_number': reference_number
    }), 200

#  GET /api/get-budget-report?start_date=2025-02-20&end_date=2025-02-27

@app.route('/api/get-budget-report', methods=['GET'])
def get_budget_report():
    # Reference to the "budget" collection
    budget_ref = db.reference("budget")
    
    # Fetch budget data
    budget_data = budget_ref.get()
    
    if not budget_data:
        return jsonify({"message": "No budget records found"}), 404
    
    # Convert dict to list for filtering
    budget_list = [{"id": key, **value} for key, value in budget_data.items()]
    
    # Date filtering
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    
    if start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400
        
        budget_list = [budget for budget in budget_list if start_date.date() <= datetime.strptime(budget["date_of_request"], "%Y-%m-%d").date() <= end_date.date()]
    
    # Summary report calculation
    total_budget_amount = sum(sum(detail.get("amount", 0) for detail in budget.get("budget_details", [])) for budget in budget_list)
    total_requests = len(budget_list)
    
    summary_report = {
        "start_date": start_date.strftime("%Y-%m-%d") if start_date else None,
        "end_date": end_date.strftime("%Y-%m-%d") if end_date else None,
        "total_budget_amount": total_budget_amount,
        "total_requests": total_requests
    }
    
    # Response structure
    return jsonify({
        "summary_report": summary_report,
        "budgets": budget_list
    })

@app.route('/api/generate-accounts', methods=['POST'])
def generate_accounts():
    try:
        data = request.get_json()
        if not data:
            return {'message': 'No data provided'}, 400  # Bad request if no data is provided
        
        general_ledger_ref = db.reference("general_ledger")
        general_ledger_ref.push(data)
        
        return {'message': 'Account added to general ledger'}, 200  # Success
    except Exception as e:
        return {'message': f'An error occurred: {str(e)}'}, 500  # Internal server error for unexpected failures


# How to use
@app.route('/api/get-accounts', methods=['GET'])
def get_accounts():
    """Fetch accounts from the general ledger with optional sorting, pagination, filtering, and search."""
    
    accounts_ref = db.reference("general_ledger")
    accounts_data = accounts_ref.get()

    if not accounts_data:
        return jsonify({"message": "No accounts found"}), 404

    # Convert Firebase dict data into a list
    accounts_list = [{"id": key, **value} for key, value in accounts_data.items()]

    # Sorting (default is ascending, 'desc' for descending)
    sort_order = request.args.get('sort', 'asc')
    if sort_order == 'desc':
        accounts_list = sorted(accounts_list, key=lambda x: x['date'], reverse=True)
    else:
        accounts_list = sorted(accounts_list, key=lambda x: x['date'])

    # Filtering by reference
    reference = request.args.get('reference')
    if reference:
        accounts_list = [acc for acc in accounts_list if acc["reference"] == reference]

    # Search functionality (search by account name, description, or reference)
    search_query = request.args.get('search', '').lower()
    if search_query:
        accounts_list = [
            acc for acc in accounts_list
            if search_query in acc["account"].lower()
            or search_query in acc["description"].lower()
            or search_query in acc["reference"].lower()
        ]

    # Pagination
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    total_records = len(accounts_list)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_accounts = accounts_list[start:end]

    return jsonify({
        "total_records": total_records,
        "current_page": page,
        "per_page": per_page,
        "total_pages": (total_records + per_page - 1) // per_page,  # Calculate total pages
        "data": paginated_accounts
    })

@app.route('/api/delete-accounts/<key>', methods=['DELETE'])
def delete_account(key):
    try:
        general_ledger_ref = db.reference("general_ledger")
        
        # Check if the entry exists by the key
        entry = general_ledger_ref.child(key).get()
        
        if not entry:
            return {'message': 'Account not found'}, 404  # Return 404 if the entry doesn't exist
        
        # Delete the entry by key
        general_ledger_ref.child(key).delete()

        return {'message': 'Account data successfully deleted'}, 200  # Success
    except Exception as e:
        return {'message': f'An error occurred: {str(e)}'}, 500  # Handle unexpected errors


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
