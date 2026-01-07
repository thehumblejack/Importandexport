import os
import re

def standardize_string(s):
    # Standardize the domain part if it exists
    s = s.replace("importiny.qodeinteractive.com", "ntestifelsitewbarra.website")
    s = s.replace("ImportExport.qodeinteractive.com", "ntestifelsitewbarra.website")
    
    # Handle both literal Unicode and URL-encoded versions
    # ﹕ -> %EF%B9%95
    # ꤷ -> %EA%A4%B7
    # ﹖ -> %EF%B9%96
    
    # Replace these with underscores
    replacements = [
        ("%EF%B9%95", "_"), ("%EA%A4%B7", "_"), ("%EF%B9%96", "_"),
        ("\xef\xb9\x95", "_"), ("\xea\xa4\xb7", "_"), ("\xef\xb9\x96", "_"),
        ("﹕", "_"), ("ꤷ", "_"), ("﹖", "_")
    ]
    
    for old, new in replacements:
        s = s.replace(old, new)
    
    # Replace any other non-ASCII or problematic characters in URLs/Filenames
    # But be careful not to break valid URL parts like '=' or '&' if we are in HTML
    # For filenames, we'll be more aggressive
    return s

def standardize_filename(filename):
    s = standardize_string(filename)
    # Aggressively clean up filenames
    standardized = re.sub(r'[^a-zA-Z0-9.\-_]', '_', s)
    standardized = re.sub(r'_{2,}', '_', standardized)
    return standardized

# Step 1: Rename files
root_dir = "wp-json/oembed/1.0"
if os.path.exists(root_dir):
    for filename in os.listdir(root_dir):
        old_path = os.path.join(root_dir, filename)
        if os.path.isfile(old_path):
            new_filename = standardize_filename(filename)
            new_path = os.path.join(root_dir, new_filename)
            if old_path != new_path:
                print(f"Renaming: {filename} -> {new_filename}")
                os.rename(old_path, new_path)

# Step 2: Update references in all files
print("Updating references in files...")
for root, dirs, files in os.walk("."):
    if ".git" in dirs:
        dirs.remove(".git")
    for file in files:
        if file.endswith((".html", ".css", ".js", ".json")):
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Check if we have any of our markers
                if any(x in content for x in ["%EF%B9%95", "%EA%A4%B7", "%EF%B9%96", "﹕", "ꤷ", "﹖", "importiny.qodeinteractive.com"]):
                    new_content = standardize_string(content)
                    if new_content != content:
                        print(f"Updating references in: {path}")
                        with open(path, "w", encoding="utf-8") as f:
                            f.write(new_content)
            except Exception as e:
                print(f"Error processing {path}: {e}")
