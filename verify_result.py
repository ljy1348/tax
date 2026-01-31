import os

filepath = r"result\20260110.C103900.1234567891"

if not os.path.exists(filepath):
    print("File not found.")
    exit(1)

print(f"File size: {os.path.getsize(filepath)} bytes")

with open(filepath, "rb") as f:
    content = f.read()

# Check distinct lines
lines = content.split(b"\r\n")
# Remove empty last line if exists due to split
if lines[-1] == b"":
    lines.pop()

print(f"Total records: {len(lines)}")

for i, line in enumerate(lines):
    print(f"\n--- Record {i + 1} ---")
    print(f"Byte Length: {len(line)}")
    try:
        decoded = line.decode("cp949")
        print(f"Decoded: {decoded}")
    except Exception as e:
        print(f"Decoding Error: {e}")
