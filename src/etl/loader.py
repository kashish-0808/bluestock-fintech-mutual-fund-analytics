import os
import pandas as pd

RAW_PATH = "data/raw"
PROCESSED_PATH = "data/processed"

def load_file(file_name):
    file_path = os.path.join(RAW_PATH, file_name)

    df = pd.read_excel(file_path, skiprows=1)

    # clean column names
    df.columns = [col.strip().replace(" ", "_") for col in df.columns]

    print("\n========================")
    print(f"File: {file_name}")
    print(f"Shape: {df.shape}")

    # SAVE CLEAN FILE
    output_file = file_name.replace(".xlsx", ".csv")
    output_path = os.path.join(PROCESSED_PATH, output_file)

    df.to_csv(output_path, index=False)

    print(f"Saved to: {output_path}")

    return df


if __name__ == "__main__":
    files = os.listdir(RAW_PATH)

    excel_files = [f for f in files if f.endswith(".xlsx")]

    print(f"Total Excel files found: {len(excel_files)}")

    for f in excel_files:
        load_file(f)

    print("\nETL Loader finished successfully 🚀")