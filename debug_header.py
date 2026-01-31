import os

# Use the file created by the user (with new taxpayer ID)
# Filename might be different now due to ID change
# Check the result directory

output_dir = "result"
files = os.listdir(output_dir)
target_file = None
for f in files:
    if f.startswith("2026"):
        target_file = os.path.join(output_dir, f)
        break

if not target_file:
    print("No result file found.")
    exit()

print(f"Inspecting: {target_file}")
print(f"File Size: {os.path.getsize(target_file)}")

with open(target_file, "rb") as f:
    content = f.read()

# First Record
first_crlf_index = content.find(b"\r\n")
if first_crlf_index == -1:
    print("No CRLF found!")
else:
    print(f"First CRLF at index: {first_crlf_index}")

record1 = content[:first_crlf_index]
print(f"Record 1 Length: {len(record1)}")
print("--- Hex Dump ---")
print(record1.hex())

# Check individual fields based on byte slicing
layout = [
    (2, "Data Type"),
    (7, "Form Code"),
    (13, "Taxpayer ID"),
    (2, "Tax Item"),
    (2, "Report Type"),
    (2, "Detail Type"),
    (3, "Kind Code"),
    (6, "Attrib YM"),
    (6, "Pay YM"),
    (6, "Submit YM"),
    (20, "User ID"),
    (5, "Minwon"),
    (10, "Agent ID"),
    (30, "Agent Name"),
    (6, "Agent Mgmt"),
    (14, "Agent Phone"),
    (30, "Comp Name"),
    (70, "Address"),
    (14, "Comp Phone"),
    (50, "Email"),
    (30, "Rep Name"),
    (2, "Src Report Type"),
    (1, "YearEnd"),
    (1, "IncomeDisp"),
    (1, "Refund"),
    (1, "Batch"),
    (1, "BizUnit"),
    (1, "SubSheet"),
    (1, "CarryOver"),
    (1, "PrePay"),
    (3, "Bank"),
    (20, "Account"),
    (8, "Date"),
    (4, "Prog Code"),
    (27, "Space"),
]

offset = 0
print("\n--- Field Parsing ---")
for length, name in layout:
    chunk = record1[offset : offset + length]
    try:
        val = chunk.decode("cp949")
    except:
        val = "[Decode Error]"
    print(f"[{offset}:{offset + length}] {name} ({length}): '{val}' hex={chunk.hex()}")
    offset += length

print(f"\nFinal Offset: {offset}")
if offset != len(record1):
    print(f"WARNING: Layout sum {offset} != Record length {len(record1)}")
