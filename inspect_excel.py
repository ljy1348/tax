import pandas as pd
import os

file_path = r"data\사업소득 원천세신고 예시.xlsx"

if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
else:
    try:
        # Load the excel file
        xl = pd.ExcelFile(file_path)
        print(f"Sheet names: {xl.sheet_names}")

        # Read the first sheet without header to find the structure
        df = xl.parse(xl.sheet_names[0], header=None)
        print("\n--- First 10 rows of data ---")
        print(df.head(10).to_string())

        print("\n--- Shape ---")
        print(df.shape)

    except Exception as e:
        print(f"Error reading excel file: {e}")
