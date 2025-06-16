from woocommerce import API
from config import WC_SITE_URL, WC_CONSUMER_KEY, WC_CONSUMER_SECRET

wcapi = API(
    url=WC_SITE_URL,
    consumer_key=WC_CONSUMER_KEY,
    consumer_secret=WC_CONSUMER_SECRET,
    version="wc/v3"
)
def get_all_products():
    try:
        response = wcapi.get("products", params={"per_page": 100})
        return response.json()
    except Exception as e:
        print(f"[ERROR] Failed to fetch products: {e}")
        return []

def hide_product(product_id):
    try:
        wcapi.put(f"products/{product_id}", {"catalog_visibility": "hidden"})
        print(f"[INFO] Product {product_id} hidden")
    except Exception as e:
        print(f"[ERROR] Failed to hide product {product_id}: {e}")
def update_product(sku, stock_quantity, price):
    data = {
        "stock_quantity": stock_quantity,
        "regular_price": str(price),
        "manage_stock": True
    }

    try:
        wcapi.put(f"products/{sku}", data)
    except Exception as e:
        print(f"[ERROR] Failed to update {sku}: {e}")