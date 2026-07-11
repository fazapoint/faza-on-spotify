import boto3
import os
from dotenv import load_dotenv
from botocore.config import Config


# load credential from .env
load_dotenv()

# 2. Establish the connection
# Note: R2 uses 'auto' for the region name, which is a required placeholder for boto3.
s3_client = boto3.client(
    service_name="s3",
    endpoint_url=f"https://{os.getenv("ACCOUNT_ID")}.r2.cloudflarestorage.com",
    aws_access_key_id=os.getenv("ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY"),
    region_name="auto", 
    config=Config(signature_version="s3v4")
)

# --- 3. Example Operations ---

# A. Upload a File
def upload_file(local_path, r2_object_name):
    try:
        s3_client.upload_file(local_path, os.getenv("BUCKET_NAME"), r2_object_name)
        print(f"Successfully uploaded {local_path} to R2 as '{r2_object_name}'")
    except Exception as e:
        print(f"Upload failed: {e}")

# B. List Objects in the Bucket
def list_files():
    try:
        response = s3_client.list_objects_v2(Bucket=os.getenv("BUCKET_NAME"))
        print("\nFiles in Bucket:")
        for obj in response.get("Contents", []):
            print(f" - {obj['Key']} ({obj['Size']} bytes)")
    except Exception as e:
        print(f"Failed to list objects: {e}")

# C. Download a File
def download_file(r2_object_name, local_destination_path):
    try:
        s3_client.download_file(os.getenv("BUCKET_NAME"), r2_object_name, local_destination_path)
        print(f"\nSuccessfully downloaded '{r2_object_name}' to {local_destination_path}")
    except Exception as e:
        print(f"Download failed: {e}")

# --- Execute Examples ---
if __name__ == "__main__":
    # Create a dummy local file to test
    with open("hello.txt", "w") as f:
        f.write("Hello from Cloudflare R2 and Python!")
        
    upload_file("hello.txt", "folder/hello_r2.txt")
    list_files()
    download_file("folder/hello_r2.txt", "downloaded_hello.txt")