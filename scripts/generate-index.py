from pathlib import Path
from html import escape
from urllib.parse import quote

ROOT = Path(".")
INDEX = ROOT / "index.html"

files_by_directory = {}

for path in ROOT.rglob("*"):
    if not path.is_file():
        continue
    if path == INDEX:
        continue
    if ".git" in path.parts or ".github" in path.parts or "scripts" in path.parts:
        continue

    # Only include uploaded HTML files.
    if path.suffix.lower() != ".html":
        continue

    directory = path.parent
    files_by_directory.setdefault(directory, []).append(path)

lines = [
    "<!doctype html>",
    '<html lang="en">',
    "<head>",
    '  <meta charset="utf-8">',
    "  <title>Mayo Archive</title>",
    "</head>",
    "<body>",
    "  <h1>Mayo Archive</h1>",
]

for directory in sorted(files_by_directory, key=lambda p: str(p).lower()):
    title = "Root" if directory == Path(".") else str(directory)
    lines.append(f"  <h2>{escape(title)}</h2>")
    lines.append("  <ul>")

    for path in sorted(files_by_directory[directory], key=lambda p: p.name.lower()):
        relative_path = path.as_posix()
        link = quote(relative_path, safe="/")
        label = escape(path.stem)
        lines.append(f'    <li><a href="{link}">{label}</a></li>')

    lines.append("  </ul>")

lines.extend([
    "</body>",
    "</html>",
    "",
])

INDEX.write_text("\n".join(lines), encoding="utf-8")
