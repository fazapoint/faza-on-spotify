import boto3
import os
import json
from dotenv import load_dotenv
from botocore.config import Config


# load credential from .env
load_dotenv()

# Establish the connection
# Note: R2 uses 'auto' for the region name, which is a required placeholder for boto3.
s3_client = boto3.client(
    service_name="s3",
    endpoint_url=f"https://{os.getenv('ACCOUNT_ID')}.r2.cloudflarestorage.com",
    aws_access_key_id=os.getenv("ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY"),
    region_name="auto", 
    config=Config(signature_version="s3v4")
)


# Upload a file locally
def upload_file_from_local(local_path, r2_object_name):
    try:
        s3_client.upload_file(local_path, os.getenv("BUCKET_NAME"), r2_object_name)
        print(f"Successfully uploaded {local_path} to R2 as '{r2_object_name}'")
    except Exception as e:
        print(f"Upload failed: {e}")

# Upload file directly json
def upload_file_from_api(json_data, r2_object_name):
    try:
        s3_client.put_object(
            Bucket=os.getenv("BUCKET_NAME"),
            Key=r2_object_name,
            Body=json_data,
            ContentType="application/json"
        )
        print(f"Successfully uploaded data directly to R2 as '{r2_object_name}'")
    except Exception as e:
        print(f"Direct upload failed: {e}")


# List objects in the bucket
def list_files():
    try:
        response = s3_client.list_objects_v2(Bucket=os.getenv("BUCKET_NAME"))
        print("\nFiles in Bucket:")
        for obj in response.get("Contents", []):
            print(f" - {obj['Key']} ({obj['Size']} bytes)")
    except Exception as e:
        print(f"Failed to list objects: {e}")

# Download a File
def download_file(r2_object_name, local_destination_path):
    try:
        s3_client.download_file(os.getenv("BUCKET_NAME"), r2_object_name, local_destination_path)
        print(f"\nSuccessfully downloaded '{r2_object_name}' to {local_destination_path}")
    except Exception as e:
        print(f"Download failed: {e}")

# Search file based on prefix
def search_file_prefix(r2_object_name, prefixes):
    response = s3_client.list_objects_v2(Bucket=os.getenv("BUCKET_NAME"), Prefix=f"{r2_object_name}/{prefix}")
    clean_json = json.dumps(response, default=str, indent=4)
    print(clean_json)

if __name__ == "__main__":
    # upload_file_from_local("hello.txt", f"{TARGET_BLOB_OBJECT}/hello_r2.txt")
    # list_files()
    # download_file(f"folder/hello_r2.txt", "downloaded_hello.txt")
    search_file_prefix('Landing/recently-played', 'spotify_raw_20260716')