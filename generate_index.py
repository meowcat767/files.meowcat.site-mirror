#!/usr/bin/env python3
import os
from pathlib import Path
from datetime import datetime

# --- Configuration ---
ROOT_DIR = Path(".")  # Where to start scanning
IGNORED_PREFIXES = ["."]  # Ignore hidden folders/files

# --- Helpers ---
def human_size(size_bytes):
    """Convert bytes to human-readable format"""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} PB"

def list_dir(directory: Path, rel_path=""):
    """Generate HTML file list for a single directory"""
    entries = []
    for entry in sorted(directory.iterdir()):
        if any(entry.name.startswith(p) for p in IGNORED_PREFIXES):
            continue
        entries.append(entry)
    return entries

def generate_html(directory: Path, rel_path=""):
    """Generate index.html for one directory"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    entries = list_dir(directory, rel_path)
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Index of /{rel_path}</title>
    <style>
        body {{ font-family: sans-serif; padding: 2rem; }}
        h1 {{ margin-bottom: 1rem; }}
        ul {{ list-style: none; padding: 0; }}
        li {{ margin: 0.5rem 0; }}
        a {{ text-decoration: none; color: #007acc; }}
        a:hover {{ text-decoration: underline; }}
        .info {{ color: #666; font-size: 0.9em; }}
    </style>
</head>
<body>
<h1>Index of /{rel_path}</h1>
<p class="info">Generated on {now}</p>
<p class="info">files.meowcat.site</p>
<ul>
"""

    # Add parent link if not at root
    if rel_path:
        html += f'    <li><a href="../">../</a></li>\n'

    # Add directories first
    for entry in entries:
        if entry.is_dir():
            html += f'    <li><a href="{entry.name}/">{entry.name}/</a></li>\n'

    # Add files
    for entry in entries:
        if entry.is_file():
            size = human_size(entry.stat().st_size)
            mtime = datetime.fromtimestamp(entry.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            html += f'    <li><a href="{entry.name}" download>{entry.name}</a> — {size}, modified {mtime}</li>\n'

    html += """
</ul>
</body>
</html>
"""
    (directory / "index.html").write_text(html)
    print(f"Generated {directory / 'index.html'}")

def generate_all(directory: Path, rel_path=""):
    """Recursively generate index.html for every directory"""
    generate_html(directory, rel_path)
    for entry in directory.iterdir():
        if entry.is_dir() and not any(entry.name.startswith(p) for p in IGNORED_PREFIXES):
            generate_all(entry, rel_path + entry.name + "/")

# --- Main ---
if __name__ == "__main__":
    generate_all(ROOT_DIR)
    print(" Yay! All index.html files generated successfully.")
