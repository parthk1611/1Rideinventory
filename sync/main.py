import csv
from ftp_downloader import download_csv
from sema_client import get_product_details
from woocommerce_client import update_product

def run_inventory_sync():
    print("[INFO] Starting inventory sync...")
    csv_file = download_csv()
    
    with open(csv_file, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            sku = row.get("SKU")
            stock = int(row.get("Stock", 0))
            price = float(row.get("Price", 0.0))

            # Optional enrichment
            sema_data = get_product_details(sku)
            # Extend logic to use sema_data if needed

            update_product(sku, stock, price)
    
    print("[INFO] Sync completed successfully.")