from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# Hardcoded credentials (VULNERABILITY)
ADMIN_PASSWORD = "admin123"
SECRET_API_KEY = "sk_live_51234567890abcdef"

# Initialize database with vulnerable setup
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT,
            email TEXT
        )
    ''')
    cursor.execute("INSERT OR IGNORE INTO users VALUES (1, 'admin', 'admin123', 'admin@example.com')")
    cursor.execute("INSERT OR IGNORE INTO users VALUES (2, 'user', 'password', 'user@example.com')")
    conn.commit()
    conn.close()

# Home page with login form
@app.route('/')
def home():
    return render_template_string('''
        <h1>Vulnerable Test Application</h1>
        <h2>Login</h2>
        <form action="/login" method="POST">
            Username: <input type="text" name="username"><br>
            Password: <input type="text" name="password"><br>
            <input type="submit" value="Login">
        </form>
        <hr>
        <h2>Search Users</h2>
        <form action="/search" method="GET">
            Search: <input type="text" name="query">
            <input type="submit" value="Search">
        </form>
        <hr>
        <h2>Comment</h2>
        <form action="/comment" method="POST">
            Name: <input type="text" name="name"><br>
            Comment: <input type="text" name="comment"><br>
            <input type="submit" value="Post">
        </form>
    ''')

# SQL Injection vulnerability
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    
    # VULNERABLE: Direct string concatenation in SQL query
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    
    try:
        cursor.execute(query)
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return f"<h2>Login Successful!</h2><p>Welcome {result[1]}!</p><p>Email: {result[3]}</p>"
        else:
            return "<h2>Login Failed</h2><p>Invalid credentials</p>"
    except Exception as e:
        return f"<h2>Error</h2><p>{str(e)}</p>"

# SQL Injection in search
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    
    # VULNERABLE: SQL injection
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    sql = f"SELECT username, email FROM users WHERE username LIKE '%{query}%'"
    
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        conn.close()
        
        html = "<h2>Search Results:</h2><ul>"
        for row in results:
            html += f"<li>{row[0]} - {row[1]}</li>"
        html += "</ul><a href='/'>Back</a>"
        return html
    except Exception as e:
        return f"<h2>Database Error</h2><p>{str(e)}</p>"

# XSS vulnerability
@app.route('/comment', methods=['POST'])
def comment():
    name = request.form.get('name', '')
    comment = request.form.get('comment', '')
    
    # VULNERABLE: No sanitization, direct output
    template = f'''
        <h2>Comment Posted!</h2>
        <p><strong>Name:</strong> {name}</p>
        <p><strong>Comment:</strong> {comment}</p>
        <a href="/">Back</a>
    '''
    return render_template_string(template)

# Exposed sensitive information
@app.route('/debug')
def debug():
    return f'''
        <h2>Debug Info (SENSITIVE DATA EXPOSED)</h2>
        <p>Admin Password: {ADMIN_PASSWORD}</p>
        <p>API Key: {SECRET_API_KEY}</p>
        <p>Database: database.db</p>
    '''

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=8080)
