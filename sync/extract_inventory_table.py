import os
from sync.config import INVENTORY_LOCAL_PATH
import pandas as pd

def extract_and_save_cleaned_inventory():
    # Path to the actual file location on macOS
    csv_path = os.path.join(INVENTORY_LOCAL_PATH, "Inventory.csv")

    df = pd.read_csv(csv_path)
    print(f"[DEBUG] Raw rows loaded: {len(df)}")

    # Normalize PartNumber: strip and uppercase
    df['PartNumber'] = df['PartNumber'].astype(str).str.strip().str.upper()
    print(f"[DEBUG] Normalized PartNumber preview:\n{df['PartNumber'].head()}")

    # Clean string fields in selected columns
    for col in ["VendorName", "Vencode", "KitComponents"]:
        df[col] = df[col].astype(str).str.strip()

    # Convert Cost and TotalQty to numeric
    df['Cost'] = pd.to_numeric(df['Cost'], errors='coerce')
    df['TotalQty'] = pd.to_numeric(df['TotalQty'], errors='coerce')

    # Select required columns
    temp_table = df[[
        "PartNumber",
        "VendorName",
        "Vencode",
        "Cost",
        "TotalQty",
        "KitComponents"
    ]]

    # Display or process the table
    print("[INFO] Temporary Inventory Table:")
    print(temp_table.head())

    # Save it as a new CSV file
    print(f"[DEBUG] Cleaned and filtered table rows: {len(temp_table)}")
    print(f"[DEBUG] Saving cleaned inventory to {os.path.join(INVENTORY_LOCAL_PATH, 'inventory_temp_table.csv')}")
    temp_table.to_csv(os.path.join(INVENTORY_LOCAL_PATH, "inventory_temp_table.csv"), index=False)

if __name__ == "__main__":
    extract_and_save_cleaned_inventory()