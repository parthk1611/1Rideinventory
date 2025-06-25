import ssl
import subprocess
from ftplib import FTP_TLS
import traceback
from config import FTP_HOST, FTP_USER, FTP_PASS, FTP_FILE

def list_ftp_files():
    print(f"[DEBUG] Running lftp to list files on {FTP_HOST}...")
    cmd = [
        "lftp",
        "-u", f"{FTP_USER},{FTP_PASS}",
        "-e", "set ssl:verify-certificate no; cls -1; bye",
        f"ftps://{FTP_HOST}"
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        files = result.stdout.strip().split("\n")
        print("[DEBUG] Files on FTP server:")
        for f in files:
            print(f)
        return files
    except subprocess.CalledProcessError as e:
        print("[FTP ERROR] lftp command failed:")
        print(e.stderr)
        raise

def download_file(filename):
    print(f"[DEBUG] Downloading {filename} from {FTP_HOST}...")
    cmd = [
        "lftp",
        "-u", f"{FTP_USER},{FTP_PASS}",
        "-e", f"set ssl:verify-certificate no; set xfer:clobber true; get {filename} -o /tmp/{filename}; bye",
        f"ftps://{FTP_HOST}"
    ]
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"[DEBUG] File downloaded to /tmp/{filename}")
        return f"/tmp/{filename}"
    except subprocess.CalledProcessError as e:
        print("[FTP ERROR] lftp download failed:")
        print(e.stderr)
        raise


# --- MASTER CSV GENERATION ---
def generate_master_csv():
    import os
    import pandas as pd
    from sync.config import FTP_FILE, INVENTORY_LOCAL_PATH

    ftp_path = f"/tmp/{FTP_FILE}"
    sema_path = os.path.join(INVENTORY_LOCAL_PATH, "sema_parts_all.csv")
    output_path = "/Users/parthkevadiya/Desktop/master_data.csv"

    ftp_df = pd.read_csv(ftp_path)
    sema_df = pd.read_csv(sema_path)

    ftp_df.rename(columns={
        "VendorName": "Brand",
        "VendorCode": "Brand Code",
        "PartNumber": "KEYSTONE PART NUMBER",
        "Cost": "KEYSTONE PRICE",
        "GreatLakesQty": "KEYSTONE LOCAL STOCK",
        "TotalQty": "KEYSTONE TOTAL STOCK",
        "LongDescription": "KEYSTONE DESCRIPTION"
    }, inplace=True)

    ftp_columns = [
        "Brand", "Brand Code", "KEYSTONE PART NUMBER", "KEYSTONE PRICE",
        "KEYSTONE LOCAL STOCK", "KEYSTONE TOTAL STOCK", "KEYSTONE DESCRIPTION",
        "KitComponents", "IsKit", "IsChemical", "UPCCode", "Prop65Toxicity", "IsNonReturnable"
    ]
    sema_columns = ["PartNumber", "MRSP", "Pictures", "Description"]

    sema_df.rename(columns={
        "PartNumber": "KEYSTONE PART NUMBER",
        "Description": "SEMA Description"
    }, inplace=True)

    ftp_df = ftp_df[ftp_columns]
    sema_df = sema_df[["KEYSTONE PART NUMBER", "MRSP", "Pictures", "SEMA Description"]]

    master_df = pd.merge(ftp_df, sema_df, on="KEYSTONE PART NUMBER", how="left")
    master_df.to_csv(output_path, index=False)
    print(f"[INFO] Master data CSV saved to: {output_path}")