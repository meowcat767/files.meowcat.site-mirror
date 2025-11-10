#!/usr/bin/env python3
import os
from pathlib import Path
from datetime import datetime

# --- Configuration ---
DOWNLOAD_DIR = Path(".")    # folder with files
OUTPUT_FILE = Path("index.html")    # output HTML file

# --- Helpers ---
def human_size(size_bytes):
    """Convert bytes to human-readable format"""
    for unit in ['B','KB','MB','GB','TB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} PB"

def generate_file_list(base_path, relative_path=""):
    """Recursively list files with size and modified date"""
    html = ""
    for f in sorted(base_path.iterdir()):
        f_rel = relative_path + f.name
        if f.is_file():
            size = human_size(f.stat().st_size)
            mtime = datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            html += f'    <li><a href="{DOWNLOAD_DIR}/{f_rel}">{f_rel}</a> — {size}, modified {mtime}</li>\n'
        elif f.is_dir():
            html += f'    <li><strong>{f_rel}/</strong></li>\n'
            html += generate_file_list(f, f_rel + "/")
    return html

# --- Generate HTML ---
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

html = f"""<!DOCTYPE html>
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

html += generate_file_list(DOWNLOAD_DIR)
html += """
</ul>
</body>
</html>
"""

# --- Write to file ---
OUTPUT_FILE.write_text(html)
print(f"Generated {OUTPUT_FILE} with all files in {DOWNLOAD_DIR}")
