from flask import Flask, request, render_template_string
import sqlite3
import logging
import sys

# Configure logging to output to console (Datadog will capture these logs)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Hardcoded credentials (VULNERABILITY)
ADMIN_PASSWORD = "admin123"
SECRET_API_KEY = "sk_live_51234567890abcdef"
CREDIT_CARD = "4532-1234-5678-9010"  # Fake credit card for testing

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
    logger.info("Database initialized successfully")

# Home page with login form
@app.route('/')
def home():
    logger.info("Home page accessed")
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
        <hr>
        <h2>Payment Test</h2>
        <form action="/payment" method="POST">
            Credit Card: <input type="text" name="card"><br>
            <input type="submit" value="Pay">
        </form>
    ''')

# SQL Injection vulnerability
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    
    # VULNERABLE: Logging sensitive data - passwords in plaintext!
    logger.warning(f"Login attempt - Username: {username}, Password: {password}")
    
    # VULNERABLE: Direct string concatenation in SQL query
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    
    try:
        cursor.execute(query)
        result = cursor.fetchone()
        conn.close()
        
        if result:
            # VULNERABLE: Logging user data including password
            logger.info(f"Successful login for user: {result[1]}, email: {result[3]}, password: {result[2]}")
            return f"<h2>Login Successful!</h2><p>Welcome {result[1]}!</p><p>Email: {result[3]}</p>"
        else:
            logger.warning("Login failed - invalid credentials")
            return "<h2>Login Failed</h2><p>Invalid credentials</p>"
    except Exception as e:
        logger.error(f"Database error during login: {str(e)}")
        return f"<h2>Error</h2><p>{str(e)}</p>"

# SQL Injection in search
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    
    logger.info(f"Search query received: {query}")
    
    # VULNERABLE: SQL injection
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    sql = f"SELECT username, email FROM users WHERE username LIKE '%{query}%'"
    
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        conn.close()
        
        # VULNERABLE: Logging email addresses
        for row in results:
            logger.info(f"Search result - Username: {row[0]}, Email: {row[1]}")
        
        html = "<h2>Search Results:</h2><ul>"
        for row in results:
            html += f"<li>{row[0]} - {row[1]}</li>"
        html += "</ul><a href='/'>Back</a>"
        return html
    except Exception as e:
        logger.error(f"Database error during search: {str(e)}")
        return f"<h2>Database Error</h2><p>{str(e)}</p>"

# XSS vulnerability
@app.route('/comment', methods=['POST'])
def comment():
    name = request.form.get('name', '')
    comment = request.form.get('comment', '')
    
    # VULNERABLE: Logging user input that might contain sensitive data
    logger.info(f"Comment posted by {name}: {comment}")
    
    # VULNERABLE: No sanitization, direct output
    template = f'''
        <h2>Comment Posted!</h2>
        <p><strong>Name:</strong> {name}</p>
        <p><strong>Comment:</strong> {comment}</p>
        <a href="/">Back</a>
    '''
    return render_template_string(template)

# NEW: Payment endpoint to test credit card detection
@app.route('/payment', methods=['POST'])
def payment():
    card = request.form.get('card', '')
    
    # VULNERABLE: Logging credit card numbers!
    logger.warning(f"Payment processing - Credit Card: {card}")
    logger.info(f"Transaction initiated with card ending in {card[-4:]}")
    
    return f'''
        <h2>Payment Processed</h2>
        <p>Card used: {card}</p>
        <a href="/">Back</a>
    '''

# Exposed sensitive information
@app.route('/debug')
def debug():
    # VULNERABLE: Logging all sensitive credentials
    logger.critical(f"DEBUG ACCESS - Admin Password: {ADMIN_PASSWORD}")
    logger.critical(f"DEBUG ACCESS - API Key: {SECRET_API_KEY}")
    logger.critical(f"DEBUG ACCESS - Test Credit Card: {CREDIT_CARD}")
    
    return f'''
        <h2>Debug Info (SENSITIVE DATA EXPOSED)</h2>
        <p>Admin Password: {ADMIN_PASSWORD}</p>
        <p>API Key: {SECRET_API_KEY}</p>
        <p>Test Credit Card: {CREDIT_CARD}</p>
        <p>Database: database.db</p>
    '''

# NEW: API endpoint that logs tokens
@app.route('/api/authenticate', methods=['POST'])
def api_auth():
    token = request.form.get('token', '')
    
    # VULNERABLE: Logging API tokens
    logger.info(f"API authentication attempt with token: {token}")
    
    if token == SECRET_API_KEY:
        logger.info(f"API authentication successful with key: {SECRET_API_KEY}")
        return {"status": "success", "message": "Authenticated"}
    else:
        logger.warning(f"API authentication failed with invalid token: {token}")
        return {"status": "error", "message": "Invalid token"}

if __name__ == '__main__':
    init_db()
    # Log startup with sensitive data
    logger.info(f"Application starting with admin password: {ADMIN_PASSWORD}")
    logger.info(f"Using API key: {SECRET_API_KEY}")
    app.run(debug=True, host='0.0.0.0', port=8080)
