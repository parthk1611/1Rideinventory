import ssl
import subprocess
from ftplib import FTP_TLS
import traceback
from sync.config import FTP_HOST, FTP_USER, FTP_PASS, FTP_FILE

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