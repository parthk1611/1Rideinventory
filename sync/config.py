import os

FTP_HOST = os.getenv("FTP_HOST", "ftp.ekeystone.com")
FTP_USER = os.getenv("FTP_USER", "S110159")
FTP_PASS = os.getenv("FTP_PASS", "dpn01oct")
FTP_FILE = os.getenv("FTP_FILE", "Inventory.csv")

SEMA_API_URL = "https://apps.semadata.org/sdapi/v2/products"
SEMA_API_KEY = os.getenv("SEMA_API_KEY", "your_sema_api_key")

WC_SITE_URL = os.getenv("WC_SITE_URL", "https://your-woocommerce-site.com")
WC_CONSUMER_KEY = os.getenv("WC_CONSUMER_KEY", "ck_xxx")
WC_CONSUMER_SECRET = os.getenv("WC_CONSUMER_SECRET", "cs_xxx")

INVENTORY_LOCAL_PATH = os.getenv("INVENTORY_LOCAL_PATH", "/Users/parthkevadiya/Downloads/1ride")