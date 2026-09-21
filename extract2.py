import json
log_path = '/Users/vrindasharma/.gemini/antigravity-ide/brain/0e73d0f3-7cfe-439a-96a4-b66281167be3/.system_generated/logs/transcript_full.jsonl'

html = ""
with open(log_path, 'r') as f:
    for line in f:
        try:
            data = json.loads(line)
            if data.get('type') == 'USER_INPUT':
                content = data.get('content', '')
                if 'Build my complete MCA project called CrediSphere AI' in content:
                    idx = content.find('<!DOCTYPE html>')
                    if idx != -1:
                        html = content[idx:]
        except:
            pass

if html:
    with open('prototype.html', 'w') as f:
        f.write(html)
    print("Successfully wrote prototype.html, length:", len(html))
else:
    print("Could not find the prototype.")
