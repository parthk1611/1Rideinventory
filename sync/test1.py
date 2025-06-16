from config import INVENTORY_LOCAL_PATH
import pandas as pd
import requests

def normalize_part_numbers(series):
    return (
        series.astype(str)
              .str.strip()
              .str.upper()
              .str.replace(r'^="(.*)"$', r'\1', regex=True)
              .str.replace(r'\s+', '', regex=True)
    )

# Config: use your actual token and brand ID
SEMA_TOKEN = "EAAAAGkHfy7iozhSKfzvOzUzMhQCI8BISyAw0eHTGBePzUch5Dg7hGNc_bk6xYBds0ukIQ"
BRAND_IDS = ["HWWK", "ZUKT", "BBGL", "FBMX", "FCLH", "FDCP"]
INVENTORY_CSV_PATH = "/tmp/Inventory.csv"

def fetch_sema_part_numbers(token: str, brand_id: str):
    url = "https://apps.semadata.org/sdapi/v2/products"
    params = {
        "token": token,
        "brandaaiaid": brand_id,
    }
    response = requests.get(url, params=params)
    if not response.ok:
        print(f"[ERROR] SEMA API returned {response.status_code}")
        print(f"[DEBUG] Response body: {response.text}")
        return []
    data = response.json()
    return [str(part).strip().upper() for part in data.get("PartNumbers", [])]

if __name__ == "__main__":
    all_parts = []
    brand_part_counts = {}
    for brand_id in BRAND_IDS:
        print(f"[INFO] Fetching parts for brand {brand_id}...")
        parts = fetch_sema_part_numbers(SEMA_TOKEN, brand_id)
        print(f"[INFO] Retrieved {len(parts)} parts for {brand_id}.")
        all_parts.extend(parts)
        all_parts_cleaned = [str(p).strip().upper() for p in all_parts]
        brand_part_counts[brand_id] = len(parts)
        # Save each brand's part numbers to a separate CSV file
        pd.DataFrame({"PartNumber": parts}).to_csv(f"{INVENTORY_LOCAL_PATH}/sema_parts_{brand_id}.csv", index=False)

    

    print("\n[SUMMARY] Parts Count Per Brand:")
    for brand, count in brand_part_counts.items():
        print(f"{brand}: {count} parts")

    print(f"\n[SUMMARY] Total Parts Retrieved: {len(all_parts)}")
    # Save all retrieved part numbers in one file
    pd.DataFrame({"PartNumber": all_parts_cleaned}).to_csv(f"{INVENTORY_LOCAL_PATH}/sema_parts_all.csv", index=False)

    # Compare with Inventory.csv and find matches
    import os
    inventory_path = os.path.join(INVENTORY_LOCAL_PATH, "Inventory.csv")
    try:
        inventory_df = pd.read_csv(inventory_path)
        inventory_df['PartNumber'] = normalize_part_numbers(inventory_df['PartNumber'])
        inventory_df = inventory_df[inventory_df['PartNumber'].notna()]
        inventory_df = inventory_df[inventory_df['PartNumber'] != ""]
        inventory_df = inventory_df[inventory_df['PartNumber'].str.len() > 2]
        inventory_df.drop_duplicates(subset="PartNumber", inplace=True)
        print(f"[INFO] Inventory parts after cleaning: {len(inventory_df)}")
        print(f"[INFO] Unique inventory parts: {inventory_df['PartNumber'].nunique()}")

        inventory_parts = set(inventory_df['PartNumber'])
        print(f"[DEBUG] Sample inventory parts: {list(inventory_parts)[:10]}")

        sema_parts = set(all_parts_cleaned)
        print(f"[DEBUG] Sample SEMA parts: {list(sema_parts)[:10]}")

        unmatched = inventory_parts - sema_parts
        print(f"[DEBUG] Sample unmatched inventory parts: {list(unmatched)[:10]}")

        matching_parts = inventory_parts & sema_parts

        # Count matches per brand
        brand_matches = {}
        for brand_id in BRAND_IDS:
            brand_df = pd.read_csv(f"{INVENTORY_LOCAL_PATH}/sema_parts_{brand_id}.csv")
            brand_df['PartNumber'] = normalize_part_numbers(brand_df['PartNumber'])
            brand_df = brand_df[brand_df['PartNumber'].notna()]
            brand_df = brand_df[brand_df['PartNumber'] != ""]
            brand_df = brand_df[brand_df['PartNumber'].str.len() > 2]
            brand_df.drop_duplicates(subset="PartNumber", inplace=True)
            print(f"[INFO] Cleaned parts for brand {brand_id}: {len(brand_df)}")
            brand_parts = set(brand_df['PartNumber'])
            matches = inventory_parts & brand_parts
            brand_matches[brand_id] = len(matches)

        print("\n[INFO] Matching parts per brand:")
        for brand, match_count in brand_matches.items():
            print(f"{brand}: {match_count} matched parts")

        print(f"\n[MATCH] Total matching parts: {len(matching_parts)}")

        # Save matches
        matched_path = os.path.join(INVENTORY_LOCAL_PATH, "matched_parts.csv")
        pd.DataFrame({"PartNumber": list(matching_parts)}).to_csv(matched_path, index=False)
        print(f"[INFO] Matching parts saved to {matched_path}")
        print(f"[SUMMARY] Total matched parts count: {len(matching_parts)}")
        print("\n[INFO] Matching parts from filtered inventory:")
        print(f"[MATCH] Total Matching Parts in filtered inventory: {len(matching_parts)}")
        print("\n[INFO] Matching parts per brand:")
        for brand, match_count in brand_matches.items():
            print(f"{brand}: {match_count} matched parts")
    except Exception as e:
        print(f"[ERROR] Failed to compare parts with inventory: {e}")
