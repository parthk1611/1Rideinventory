import pandas as pd

# Paths to the two files
csv_file_1 = "/Users/parthkevadiya/Downloads/1ride/Inventory.csv"
excel_file_2 = "/Users/parthkevadiya/Downloads/Master DATA.xlsx"

try:
    # Load CSV file normally
    df1 = pd.read_csv(csv_file_1, nrows=0)
    columns_1 = set(df1.columns)

    # List sheet names to confirm what's inside the Excel file
    sheet_names = pd.ExcelFile(excel_file_2).sheet_names
    print(f"[INFO] Available Excel sheets: {sheet_names}")

    # Load correct sheet and skip rows if necessary (adjust as needed)
    df2 = pd.read_excel(excel_file_2, sheet_name="Sheet1", skiprows=1)
    df2.columns = df2.columns.map(str).str.strip()
    columns_2 = set(df2.columns)

    # Compare and print
    print("Columns in first CSV file:")
    print(columns_1)

    print("\nColumns in second Excel file:")
    print(columns_2)

    print("\nCommon columns:")
    print(columns_1 & columns_2)

    print("\nColumns only in first CSV:")
    print(columns_1 - columns_2)

    print("\nColumns only in second Excel file:")
    print(columns_2 - columns_1)

except Exception as e:
    print(f"[ERROR] Failed to load or compare columns: {e}")