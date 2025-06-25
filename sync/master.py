import pandas as pd

# Load the CSV file from the /tmp directory
csv_path = "/Users/parthkevadiya/Downloads/1ride/Inventory.csv"
try:
    df = pd.read_csv(csv_path)
    print("[INFO] Preview of the CSV file:")
except Exception as e:
    print(f"[ERROR] Failed to load or print CSV: {e}")

# Define the columns to retain
required_columns = [
    'VendorName', 'Vencode', 'PartNumber', 'Cost', 'GreatLakesQty', 'TotalQty', 'LongDescription', 'IsNonReturnable', 'Prop65Toxicity', 'UPCCode', 'IsChemical', 'KitComponents', 'IsKit'
]

# Rename columns
rename_map = {
    'VendorName': 'BRAND',
    'Vencode': 'BRAND CODE',
    'PartNumber': 'KEYSTONE PART NUMBER',
    'Cost': 'KEYSTONE PRICE',
    'GreatLakesQty': 'KEYSTONE LOCAL STOCK',
    'TotalQty': 'KEYSTONE TOTAL STOCK',
    'LongDescription': 'KEYSTONE DESCRIPTION'
}

# Filter the DataFrame and save to a new CSV file
filtered_path = "/Users/parthkevadiya/Desktop/1RIDE/Data/filtered_ftp.csv"
try:
    filtered_df = df[required_columns].rename(columns=rename_map)
    filtered_df.insert(filtered_df.columns.get_loc('BRAND CODE') + 1, 'ManufacturerPartNo', '')
    filtered_df.insert(filtered_df.columns.get_loc('ManufacturerPartNo') + 1, 'CATEGORY 1', '')
    filtered_df.insert(filtered_df.columns.get_loc('CATEGORY 1') + 1, 'CATEGORY 1 CODE', '')
    filtered_df.insert(filtered_df.columns.get_loc('CATEGORY 1 CODE') + 1, 'CATEGORY 2', '')
    filtered_df.insert(filtered_df.columns.get_loc('CATEGORY 2') + 1, 'CATEGORY 2 CODE', '')
    filtered_df.insert(filtered_df.columns.get_loc('CATEGORY 2 CODE') + 1, 'CATEGORY 3', '')
    filtered_df.insert(filtered_df.columns.get_loc('CATEGORY 3') + 1, 'CATEGORY 3 CODE', '')
    filtered_df['Picture'] = ''
    filtered_df['long description'] = ''
    filtered_df.insert(filtered_df.columns.get_loc('UPCCode') + 1, 'Weight', '')
    filtered_df.insert(filtered_df.columns.get_loc('Weight') + 1, 'Height', '')
    filtered_df.insert(filtered_df.columns.get_loc('Height') + 1, 'Length', '')
    filtered_df.insert(filtered_df.columns.get_loc('Length') + 1, 'Width', '')
    filtered_df.to_csv(filtered_path, index=False)
    print(f"[INFO] Filtered CSV file saved to: {filtered_path}")
except KeyError as ke:
    print(f"[ERROR] One or more required columns not found: {ke}")
except Exception as e:
    print(f"[ERROR] Failed to save filtered CSV: {e}")
