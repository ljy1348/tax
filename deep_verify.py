import os
import binascii

output_dir = "result"
files = [f for f in os.listdir(output_dir) if f.startswith("2026")]
if not files:
    print("No file found")
    exit()

# Sort by mod time to get latest
files.sort(key=lambda x: os.path.getmtime(os.path.join(output_dir, x)), reverse=True)
target = os.path.join(output_dir, files[0])
print(f"Target: {target}")

with open(target, "rb") as f:
    data = f.read()

total_len = len(data)
print(f"Total Bytes: {total_len}")

# Split by CRLF
records = data.split(b"\r\n")
# If last CRLF exists, last item is empty
if records[-1] == b"":
    records.pop()

print(f"Records found: {len(records)}")

for i, rec in enumerate(records):
    print(f"Record {i + 1} Length: {len(rec)}")
    if i == 0 and len(rec) != 400:
        print(f"Expected 400, got {len(rec)}")
    if i > 0 and len(rec) != 150:
        print(f"Expected 150, got {len(rec)}")

    # Hex dump first 50 bytes and last 50 bytes of record 1
    if i == 0:
        print(f"Head: {binascii.hexlify(rec[:50])}")
        print(f"Tail: {binascii.hexlify(rec[-50:])}")
