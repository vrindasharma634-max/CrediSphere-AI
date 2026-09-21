import re
log_path = '/Users/vrindasharma/.gemini/antigravity-ide/brain/0e73d0f3-7cfe-439a-96a4-b66281167be3/.system_generated/logs/transcript_full.jsonl'

with open(log_path, 'r') as f:
    full_text = f.read()

# The HTML was injected right after </ADDITIONAL_METADATA>
# Find the exact occurrence that leads to the HTML
match = re.search(r'</ADDITIONAL_METADATA>\\n(<!DOCTYPE html>.*?</html>)', full_text, re.DOTALL)
if match:
    html = match.group(1)
    # the JSON string has escaped newlines, so we must unescape them
    html = html.replace('\\n', '\n').replace('\\"', '"').replace('\\t', '\t')
    with open('prototype.html', 'w') as f:
        f.write(html)
    print("Extracted prototype.html from raw transcript! Length:", len(html))
else:
    print("Could not find the prototype using raw regex.")
