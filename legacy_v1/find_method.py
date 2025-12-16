
with open("main.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        if "def refresh_explorer" in line:
            print(f"Found at line {i+1}: {line.strip()}")
