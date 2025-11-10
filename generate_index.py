import os
from pathlib import Path
from datetime import datetime

DOWNLOAD_DIR = Path("downloads")
OUTPUT_FILE = Path("index.html")

files = sorted(DOWNLOAD_DIR.iterdir())

# Get the current timestamp
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Meowcat Files - files.meowcat.site</title>
    <style>
        body {{ font-family: sans-serif; padding: 2rem; }}
        h1 {{ text-align: center; }}
        ul {{ list-style: none; padding: 0; }}
        li {{ margin: 0.5rem 0; }}
        a {{ text-decoration: none; color: #007acc; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
<h1>Meowcat Files - files.meowcat.site</h1>
<p><em>This page was last generated at: {now}</em></p>
<ul>
"""

for f in files:
    if f.is_file():
        html += f'    <li><a href="{DOWNLOAD_DIR}/{f.name}">{f.name}</a></li>\n'

html += """
</ul>
</body>
</html>
"""

OUTPUT_FILE.write_text(html)
print(f"Generated {OUTPUT_FILE} with {len(files)} files.")
