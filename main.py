import os
from src.sample_data import get_sample_data
from src.generator import TaxReturnGenerator


def main():
    print("Generating tax return file...")

    # 1. Get Data
    data = get_sample_data()
    print(f"Loaded data for company: {data.header.corp_name}")
    print(f"Number of summary records: {len(data.summaries)}")

    # 2. Generate
    generator = TaxReturnGenerator()
    try:
        file_bytes = generator.generate(data)
        print(f"Generated {len(file_bytes)} bytes.")
    except Exception as e:
        print(f"Error during generation: {e}")
        return

    # 3. Save
    output_dir = "result"
    os.makedirs(output_dir, exist_ok=True)

    # 파일명 규칙: 일자(8) + 서식코드(7) + "." + 신고구분상세코드(2)
    # 예: 20260110C103900.01
    filename = f"{data.header.write_date}{data.header.form_code}.{data.header.report_detail_type}"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "wb") as f:
        f.write(file_bytes)

    print(f"File saved to: {filepath}")


if __name__ == "__main__":
    main()
