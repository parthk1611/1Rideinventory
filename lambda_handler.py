from sync.ftp_downloader import list_ftp_files, download_file


def lambda_handler(event=None, context=None):
    print("[INFO] Starting FTP file listing...")
    try:
        files = list_ftp_files()
        print("[INFO] Files on FTP server:")
        for f in files:
            print(f)
        downloaded_path = download_file("Inventory.csv")
        print(f"[INFO] Inventory.csv downloaded to: {downloaded_path}")


        return {"status": "success", "files": files, "downloaded_file": downloaded_path}
    except Exception as e:
        print(f"[ERROR] {e}")
        return {"status": "error", "message": str(e)}

# Ensure it runs when the script is called directly
if __name__ == "__main__":
    lambda_handler()