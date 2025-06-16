import requests
from .config import SEMA_API_URL, SEMA_API_KEY

def get_product_details(part_number):
    headers = {"Authorization": f"Bearer {SEMA_API_KEY}"}
    resp = requests.get(f"{SEMA_API_URL}{part_number}", headers=headers)
    return resp.json() if resp.status_code == 200 else {}