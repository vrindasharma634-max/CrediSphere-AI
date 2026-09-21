import json
import re
import os
from bs4 import BeautifulSoup

log_path = '/Users/vrindasharma/.gemini/antigravity-ide/brain/0e73d0f3-7cfe-439a-96a4-b66281167be3/.system_generated/logs/transcript_full.jsonl'
html_content = ''

print("Reading transcript...")
try:
    with open(log_path, 'r') as f:
        for line in f:
            try:
                data = json.loads(line)
            except Exception:
                continue
            
            def search_dict(d):
                global html_content
                if isinstance(d, dict):
                    for k, v in d.items():
                        search_dict(v)
                elif isinstance(d, list):
                    for item in d:
                        search_dict(item)
                elif isinstance(d, str):
                    if '<!DOCTYPE html>' in d and 'CrediSphere AI — Product Prototype' in d:
                        match = re.search(r'(<!DOCTYPE html>.*?</html>)', d, re.DOTALL)
                        if match:
                            html_content = match.group(1)
            search_dict(data)
            if html_content:
                break
except Exception as e:
    print("Error reading:", e)

if not html_content:
    print("Failed to find HTML")
    exit(1)

print("Found HTML prototype, length:", len(html_content))
with open('prototype.html', 'w') as f:
    f.write(html_content)
# 1. Extract CSS
css_match = re.search(r'<style>(.*?)</style>', html_content, re.DOTALL)
if css_match:
    with open('frontend/css/style.css', 'w') as f:
        f.write(css_match.group(1).strip())
    print("Extracted CSS")

# 2. Extract pages
mapping = {
    'frame-login': 'login.html',
    'frame-signup': 'signup.html',
    'frame-admin': 'admin-dashboard.html',
    'frame-credit': 'credit-intelligence.html',
    'frame-collections': 'collections-ai.html',
    'frame-user': 'customer-dashboard.html',
    'frame-apply': 'loan-application.html',
    'frame-policy': 'risk-policy.html',
    'frame-reports': 'reports.html',
    'frame-kyc': 'kyc-upload.html',
    'frame-screenconfig': 'screen-configuration.html'
}

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CrediSphere AI</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../css/style.css">
</head>
<body>
    {content}
    <script src="../js/api.js"></script>
    <script src="../js/app.js"></script>
    {extra_script}
</body>
</html>"""

soup = BeautifulSoup(html_content, 'html.parser')
frames = soup.find_all('div', class_='frame')
print(f"Found {len(frames)} frames")

for frame in frames:
    fid = frame.get('id')
    if fid in mapping:
        inner_html = "".join(str(c) for c in frame.children)
        
        # fix links
        for k, v in mapping.items():
            short_id = k.replace('frame-', '')
            inner_html = re.sub(fr'onclick="showFrameById\(\'{short_id}\'\)"', f'href="{v}"', inner_html)
            inner_html = re.sub(fr'onclick="showFrameById\(\'{short_id}\', this\)"', f'href="{v}"', inner_html)
            inner_html = re.sub(fr'onclick="scSwitchScreen\(\'{short_id}\', this\)"', f'href="{v}"', inner_html)

        inner_soup = BeautifulSoup(inner_html, 'html.parser')
        
        # turn sidebar items into a tags
        for sb_item in inner_soup.find_all('div', class_='sb-item'):
            if sb_item.has_attr('href'):
                sb_item.name = 'a'
                sb_item['style'] = "text-decoration:none;"

        # specific page tweaks
        extra_script = ""
        if fid == 'frame-login':
            form_side = inner_soup.find('div', class_='auth-card')
            if form_side:
                form_tag = inner_soup.new_tag('form', id='login-form')
                inputs = form_side.find_all('input')
                if len(inputs) >= 2:
                    inputs[0]['id'] = 'email'
                    inputs[1]['id'] = 'password'
                btn = form_side.find('button', class_='btn-primary')
                if btn:
                    btn['id'] = 'login-btn'
            extra_script = '<script src="../js/auth.js"></script>'
            
        final_html = html_template.format(content=str(inner_soup), extra_script=extra_script)
        with open(f"frontend/pages/{mapping[fid]}", 'w') as f:
            f.write(final_html)
        print(f"Wrote {mapping[fid]}")

# Script
script_match = re.search(r'<script>(.*?)</script>', html_content, re.DOTALL)
if script_match:
    with open('frontend/js/app.js', 'w') as f:
        f.write(script_match.group(1))
    print("Extracted app.js")
