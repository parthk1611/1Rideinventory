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

# Output results

print(f"\nTotal unique part numbers fetched: {len(all_parts_set)}")
print(f"Total matches found in Excel: {len(matched_parts)}")

# Group matched parts by brand
brand_part_lists = {}
for brand_id in BRAND_IDS:
    brand_parts_set = set([p.strip().upper() for p in fetch_part_numbers(SEMA_TOKEN, brand_id)])
    brand_part_lists[brand_id] = matched_parts[matched_parts['ManufacturerPartNo'].isin(brand_parts_set)]['ManufacturerPartNo'].unique().tolist()

print("Brand part lists:", brand_part_lists)

# Create brand-specific variables with matched part numbers
HWWK_matched_parts = brand_part_lists.get("/nHWWK", [])
ZUKT_matched_parts = brand_part_lists.get("/nZUKT", [])
BBGL_matched_parts = brand_part_lists.get("/nBBGL", [])
FBMX_matched_parts = brand_part_lists.get("/nFBMX", [])
FCLH_matched_parts = brand_part_lists.get("/nFCLH", [])
FDCP_matched_parts = brand_part_lists.get("/nFDCP", [])

brand_digital_assets = {}

for brand_id, parts in brand_part_lists.items():
    brand_digital_assets[brand_id] = {}
    for part in parts:
        response = requests.get(
            "https://apps.semadata.org/sdapi/v2/products/digitalasset",
            params={
                "token": SEMA_TOKEN,
                "brandaaiaid": brand_id,
                "partnumber": part
            }
        )
        if response.status_code == 200:
            try:
                data = response.json()
                assets = data.get("Assets", [])
                if assets:
                    image_asset = next((a.get("Value") for a in assets if a.get("FileType") in ["JPG", "PNG"] and a.get("Value")), "")
                    brand_digital_assets[brand_id][part] = image_asset
                else:
                    brand_digital_assets[brand_id][part] = ""
            except Exception as e:
                print(f"Failed to parse JSON for {brand_id} {part}: {e}")
                brand_digital_assets[brand_id][part] = ""
        else:
            print(f"Failed to fetch asset for {brand_id} {part} - Status: {response.status_code}")
            brand_digital_assets[brand_id][part] = ""

# Print assets summary
for brand_id, assets in brand_digital_assets.items():
    print(f"\nDigital assets for brand {brand_id}:")
    for part, url in assets.items():
        print(f"{part}: {url}")
