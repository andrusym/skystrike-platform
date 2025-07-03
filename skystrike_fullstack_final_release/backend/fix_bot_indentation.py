import pathlib

BOT_DIR = pathlib.Path("backend/bots")

for path in BOT_DIR.glob("*.py"):
    print(f"🔍 Fixing {path.name}")

    with path.open("r", encoding="utf-8") as f:
        lines = f.readlines()

    fixed_lines = []
    for line in lines:
        # Normalize tabs to 4 spaces and strip trailing whitespace
        line = line.replace("\t", "    ").rstrip()
        fixed_lines.append(line)

    # Detect smallest indent level (other than 0) for re-alignment
    min_indent = None
    for line in fixed_lines:
        if line.strip() and line.startswith(" "):
            indent_len = len(line) - len(line.lstrip())
            if min_indent is None or (0 < indent_len < min_indent):
                min_indent = indent_len

    # Adjust lines with bad indentation
    if min_indent:
        for i in range(len(fixed_lines)):
            line = fixed_lines[i]
            if line.strip() and line.startswith(" "):
                current_indent = len(line) - len(line.lstrip())
                if current_indent % min_indent != 0:
                    clean_indent = (current_indent // min_indent) * min_indent
                    print(f"⚠️  Adjusting indent in {path.name} line {i+1}")
                    fixed_lines[i] = " " * clean_indent + line.lstrip()

    # Write cleaned result
    with path.open("w", encoding="utf-8") as f:
        f.write("\n".join(fixed_lines) + "\n")
