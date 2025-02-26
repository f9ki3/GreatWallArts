from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import requests

app = Flask(__name__)
app.secret_key = '#@jhkasjahs'  # Required for session management

@app.route('/')
def RouteLogin():
    if 'user' not in session:  # Check if user is logged in
        return render_template('pages/index.html')       
    return redirect(url_for('dashboard'))

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
    
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
