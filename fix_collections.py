import re
import os

PROTOTYPE_PATH = "/Users/vrindasharma/Desktop/CREDISPEHERAI-PROJECT/prototype.html.bak"
if not os.path.exists(PROTOTYPE_PATH):
    PROTOTYPE_PATH = "/Users/vrindasharma/Desktop/CREDISPEHERAI-PROJECT/prototype.html"

with open(PROTOTYPE_PATH, 'r', encoding='utf-8') as f:
    clean_html = f.read()

print("Original length:", len(clean_html))
