from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Vulnerable DB connection
def get_db():
    conn = sqlite3.connect('vulnerable.db')
    return conn

# Init DB
@app.route('/init', methods=['GET'])
def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS users")
    c.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    c.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin123')")
    conn.commit()
    return "Database initialized."

# ❌ VULNERABLE: SQL Injection
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    print("[DEBUG] SQL Query:", query)
    conn = get_db()
    c = conn.cursor()
    c.execute(query)
    user = c.fetchone()
    if user:
        return jsonify({"message": "Login successful!"})
    else:
        return jsonify({"message": "Login failed!"}), 401

# ❌ VULNERABLE: Reflected XSS
@app.route('/greet', methods=['GET'])
def greet():
    name = request.args.get('name')
    return f"<h1>Hello {name}!</h1>"

# ❌ VULNERABLE: No auth on sensitive endpoint
@app.route('/admin', methods=['GET'])
def admin():
    return jsonify({"secret": "Top Secret Configs!"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
