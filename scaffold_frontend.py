import os

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CrediSphere AI - {title}</title>
    <link rel="stylesheet" href="../css/style.css">
</head>
<body>
    <div id="app">
        <nav>
            <h1>CrediSphere AI</h1>
            <div id="nav-links">
                <!-- Navigation inserted by JS -->
            </div>
        </nav>
        <main>
            <h2>{title}</h2>
            <div id="content">
                <!-- Content goes here -->
            </div>
        </main>
    </div>
    <script src="../js/api.js"></script>
    <script src="../js/app.js"></script>
</body>
</html>"""

pages = [
    "login", "signup", "customer-dashboard", "loan-application", "kyc-upload", 
    "loan-offers", "loan-tracking", "admin-dashboard", "credit-intelligence", 
    "collections-ai", "customers", "reports", "risk-policy", "screen-configuration"
]

css_files = ["style.css", "auth.css", "dashboard.css", "forms.css", "responsive.css"]
js_files = ["app.js", "auth.js", "customer.js", "loan.js", "kyc.js", "credit.js", "collections.js", "reports.js", "policy.js", "screen-config.js", "api.js"]

os.makedirs("frontend/pages", exist_ok=True)
os.makedirs("frontend/css", exist_ok=True)
os.makedirs("frontend/js", exist_ok=True)

# Generate index.html (Redirect to login)
with open("frontend/index.html", "w") as f:
    f.write("""<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="refresh" content="0; url=pages/login.html" />
</head>
<body>
    <p><a href="pages/login.html">Redirecting to Login...</a></p>
</body>
</html>""")

# Generate HTML pages
for page in pages:
    title = page.replace("-", " ").title()
    with open(f"frontend/pages/{page}.html", "w") as f:
        f.write(html_template.format(title=title))

# Generate CSS files
for css in css_files:
    with open(f"frontend/css/{css}", "w") as f:
        if css == "style.css":
            f.write("""
:root {
    --primary: #3b82f6;
    --secondary: #10b981;
    --background: #0f172a;
    --surface: rgba(30, 41, 59, 0.7);
    --text: #f8fafc;
    --text-muted: #94a3b8;
    --danger: #ef4444;
}
body {
    margin: 0;
    font-family: 'Inter', sans-serif;
    background-color: var(--background);
    color: var(--text);
}
nav {
    display: flex;
    justify-content: space-between;
    padding: 1rem 2rem;
    background: var(--surface);
    backdrop-filter: blur(10px);
    border-bottom: 1px solid rgba(255,255,255,0.1);
}
main {
    padding: 2rem;
}
.glass-card {
    background: var(--surface);
    border-radius: 12px;
    padding: 1.5rem;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.1);
}
""")
        else:
            f.write(f"/* {css} */\n")

# Generate JS files
for js in js_files:
    with open(f"frontend/js/{js}", "w") as f:
        if js == "api.js":
            f.write("""
const API_BASE = 'https://credisphere-ai.onrender.com/api';
async function apiCall(endpoint, method = 'GET', data = null) {
    const token = localStorage.getItem('token');
    const headers = {
        'Content-Type': 'application/json',
        ...(token ? { 'Authorization': `Bearer ${token}` } : {})
    };
    const config = { method, headers };
    if (data) config.body = JSON.stringify(data);
    try {
        const res = await fetch(`${API_BASE}${endpoint}`, config);
        const json = await res.json();
        if (!res.ok) throw new Error(json.error || 'API Error');
        return json;
    } catch (e) {
        console.error('API Call Failed:', e);
        throw e;
    }
}
""")
        else:
            f.write(f"// {js} logic\n")

print("Scaffolded frontend")
