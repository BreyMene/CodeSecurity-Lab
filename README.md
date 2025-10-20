# CodeSecurity-Lab

A laboratory for learning web security vulnerabilities and practicing with Datadog Code Security.

⚠️ **WARNING**: This code contains intentional vulnerabilities. DO NOT use in production.

## Project Structure

Current files in the repository:
- `app.py` - Flask application with vulnerable endpoints (SQL injection, XSS, etc.)
- `requirements.txt` - Pinned dependencies with specific versions for compatibility

## Vulnerabilities Demonstrated

1. SQL Injection
   - Via string-formatted queries in login endpoint
   - Example: `' OR 1=1 --` in password field

2. Cross-Site Scripting (XSS)
   - Through unsanitized search input
   - Example: `<script>alert('XSS')</script>`

3. Hardcoded Credentials
   - API keys and passwords in source code
   - Demo user credentials in plain text

## Setup

1. Create and activate a virtual environment:

### **Windows:**
```powershell
python -m venv venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate
```

### **Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```powershell
pip install -r requirements.txt
```

3. Run the application:
```powershell
python app.py
```

4. Access at: `http://127.0.0.1:8080`

## Dependency Versions

This project uses specific versions for compatibility:
```
Flask==3.0.0
```

## Troubleshooting

If you see ImportErrors about missing functions:
1. Delete existing virtualenv: `rm -r venv`
2. Create fresh environment with exact versions (see setup steps above)

## Testing Vulnerabilities

### SQL Injection
- username=admin, password=`' OR 1=1 --`

### XSS
- Comment: `<script>alert('XSS')</script>`

### Exposed Credentials
- URL `http://127.0.0.1:8080/debug`
## Datadog Security Analysis

Expected detections:
- SQL query string formatting
- Reflected XSS vulnerabilities
- Hardcoded secrets
- Sensitive Data Exposed 

## Author
Breyner Felipe Meneses Muñoz
<a href="https://github.com/BreyMene/BreyMene">

## License
This project is licensed under the MIT License - see the `LICENSE` file for details.

Intended for educational and testing purposes only.
