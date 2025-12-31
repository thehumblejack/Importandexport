import os
import re

html_path = "index.html"
if not os.path.exists(html_path):
    print("index.html not found")
    exit()

with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

# Find all href and src attributes with relative paths
# We look for something that doesn't start with http, https, #, mailto, tel
paths = re.findall(r'(?:href|src)=["\'](?!https?://|#|mailto:|tel:)([^"\']+)["\']', content)

missing = []
for path in paths:
    # Remove query strings and fragments
    clean_path = path.split('?')[0].split('#')[0]
    
    # Check if file exists
    if not os.path.exists(clean_path) and clean_path != "" and clean_path != "/":
        missing.append(path)

if missing:
    print(f"Found {len(missing)} missing local files:")
    for m in missing:
        print(f"  - {m}")
else:
    print("All local assets found!")
