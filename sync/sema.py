import requests

# Replace with your actual token and brand IDs
SEMA_TOKEN = "EAAAAGkHfy7iozhSKfzvOzUzMhQCI8BISyAw0eHTGBePzUch5Dg7hGNc_bk6xYBds0ukIQ"
BRAND_IDS = ["HWWK", "ZUKT", "BBGL", "FBMX", "FCLH", "FDCP"]

def fetch_part_numbers(token, brand_id):
    url = "https://apps.semadata.org/sdapi/v2/products"
    params = {
        "token": token,
        "brandaaiaid": brand_id
    }
    response = requests.get(url, params=params)
    print(f"Response for brand {brand_id}: {response.status_code}")
    try:
        data = response.json()
        print(f"Raw JSON for {brand_id}:\n{data}")
        part_numbers = data.get("PartNumbers", [])
        return part_numbers
    except Exception as e:
        print(f"Error parsing JSON for {brand_id}: {e}")
        return []

# Fetch part numbers for all brand IDs
all_parts = []
for brand_id in BRAND_IDS:
    print(f"Fetching parts for brand: {brand_id}")
    parts = fetch_part_numbers(SEMA_TOKEN, brand_id)
    print(f"Found {len(parts)} parts for {brand_id}")
    all_parts.extend(parts)

print(f"Total parts collected: {len(all_parts)}")
print(all_parts)
print(f"Unique part numbers fetched: {len(set(all_parts))}")

import pandas as pd

# Excel file path
EXCEL_PATH = "/Users/parthkevadiya/Downloads/MASTER DATA (1).xlsx"

# Load Excel file
df = pd.read_excel(EXCEL_PATH, dtype=str)

# Clean data
df['ManufacturerPartNo'] = df['ManufacturerPartNo'].str.strip().str.upper()
all_parts_set = set([p.strip().upper() for p in all_parts])

# Match part numbers
matched_parts = df[df['ManufacturerPartNo'].isin(all_parts_set)]

# Build dictionary of brand to matched part numbers
matched_dict = {}
for brand_id in BRAND_IDS:
    brand_parts = set(fetch_part_numbers(SEMA_TOKEN, brand_id))
    matched = [part for part in matched_parts['ManufacturerPartNo'] if part in brand_parts]
    if matched:
        matched_dict[brand_id] = matched

print("\nMatched Part Numbers by Brand:")
print(matched_dict)

# Output results

print(f"\nTotal unique part numbers fetched: {len(all_parts_set)}")
print(f"Total matches found in Excel: {len(matched_parts)}")

print("\nMatched Part Numbers:")
print(matched_parts['ManufacturerPartNo'].tolist())

import time

OUTPUT_XLSX_PATH = "/Users/parthkevadiya/Desktop/1RIDE/Data/master_with_pictures.xlsx"

# Load Excel again for update
df = pd.read_excel(EXCEL_PATH, dtype=str)
df['ManufacturerPartNo'] = df['ManufacturerPartNo'].str.strip().str.upper()

# Add Picture column if not present
if 'Picture' not in df.columns:
    df['Picture'] = ''

def fetch_digital_assets_export(token, brand_id, part_numbers):
    url = "https://apps.semadata.org/sdapi/v2/export/digitalassets"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "token": token,
        "AAIA_BrandId": brand_id
    }
    for i, pn in enumerate(part_numbers):
        data[f"partNumbers[{i}]"] = pn
    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        return response.json().get("DigitalAssets", [])
    except Exception as e:
        print(f"[ERROR] Digital asset fetch failed for {brand_id}: {e}")
        return []

# Fetch assets and update dataframe
for brand_id, part_list in matched_dict.items():
    print(f"[INFO] Fetching digital assets for brand: {brand_id} ({len(part_list)} parts)")
    chunk_size = 20
    for i in range(0, len(part_list), chunk_size):
        chunk = part_list[i:i+chunk_size]
        assets = fetch_digital_assets_export(SEMA_TOKEN, brand_id, chunk)
        asset_map = {}
        for asset in assets:
            part_num = asset['PartNumber'].strip().upper()
            if asset['AssetTypeCode'] in ["P04", "ZZ1", "ZZ2", "ZZ3", "ZZ4", "ZZ5"]:
                asset_map.setdefault(part_num, []).append(asset['Link'])
        for idx, row in df.iterrows():
            pn = str(row['ManufacturerPartNo']).strip().upper()
            if pn in asset_map:
                df.at[idx, 'Picture'] = "; ".join(asset_map[pn])
        time.sleep(1)

# Save updated file
df.to_excel(OUTPUT_XLSX_PATH, index=False)
print(f"[INFO] Updated Excel saved to {OUTPUT_XLSX_PATH}")
