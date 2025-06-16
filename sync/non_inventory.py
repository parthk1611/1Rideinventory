from woocommerce_client import get_all_products, hide_product
import pandas as pd

# Load Inventory.csv
df = pd.read_csv("/Users/parthkevadiya/Downloads/1ride/Inventory.csv")
inventory_skus = set(df['PartNumber'].astype(str).str.strip().str.upper())

# Loop through WooCommerce products
products = get_all_products()
for product in products:
    sku = product.get("sku", "").strip().upper()
    product_id = product.get("id")

    if sku and sku not in inventory_skus:
        hide_product(product_id)