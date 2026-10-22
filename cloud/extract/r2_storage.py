import boto3
import os
import json
from dotenv import load_dotenv
from botocore.config import Config
import re


# load credential from .env
load_dotenv()

BUCKET_NAME = os.getenv("BUCKET_NAME")

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
        s3_client.upload_file(local_path, BUCKET_NAME, r2_object_name)
        print(f"Successfully uploaded {local_path} to R2 as '{r2_object_name}'")
    except Exception as e:
        print(f"Upload failed: {e}")

# Upload file directly json
def upload_file_from_api(json_data, r2_object_name):
    try:
        s3_client.put_object(
            Bucket=BUCKET_NAME,
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
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
        print("\nFiles in Bucket:")
        for obj in response.get("Contents", []):
            print(f" - {obj['Key']} ({obj['Size']} bytes)")
    except Exception as e:
        print(f"Failed to list objects: {e}")

# Download a File
def download_file(r2_object_name, local_destination_path):
    try:
        s3_client.download_file(BUCKET_NAME, r2_object_name, local_destination_path)
        print(f"\nSuccessfully downloaded '{r2_object_name}' to {local_destination_path}")
    except Exception as e:
        print(f"Download failed: {e}")

# Search file based on prefix
def search_file_prefix(r2_object_name, prefixes):
    # hold files name
    results = []

    # loop the prefixes and extend it to iterable result
    for prefix in prefixes:
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=f"{r2_object_name}/{prefix}")
        if 'Contents' not in response:
            continue

        results.extend(response["Contents"])

    return results

def organize_r2_files_by_date_on_demand(r2_object_name):
    prefix_path = f"{r2_object_name.strip('/')}/" if r2_object_name else ""

    # List objects in the bucket matching the prefix
    paginator = s3_client.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=BUCKET_NAME, Prefix=prefix_path)

    # Regex pattern to match filenames like: spotify_raw_YYYYMMDD_HHMMSS.json
    pattern = re.compile(r".*?spotify_raw_(\d{8})_\d{6}\.json$")

    for page in pages:
        if 'Contents' not in page:
            continue

        for obj in page['Contents']:
            old_key = obj['Key']
            filename = old_key.split('/')[-1]
            
            match = pattern.match(filename)
            if match:
                date_str = match.group(1) # Extracts YYYYMMDD
                
                # Construct the new POSIX key path
                # Result: Landing/recently-played/20260713/spotify_raw_20260713_143630.json
                new_key = f"{prefix_path}{date_str}/{filename}"
                
                # Skip if the file is already inside its date folder
                if old_key == new_key:
                    continue

                print(f"Moving: {old_key} \n  --> {new_key}\n")

                # 1. Copy object to the new key
                s3_client.copy_object(
                    Bucket=BUCKET_NAME,
                    CopySource={'Bucket': BUCKET_NAME, 'Key': old_key},
                    Key=new_key
                )

                # 2. Delete the old unorganized object
                s3_client.delete_object(
                    Bucket=BUCKET_NAME,
                    Key=old_key
                )

    print("R2 bucket reorganization complete!")

def fix_messy_r2_paths(folder_base="Landing/recently-played"):
    clean_base = folder_base.strip('/')
    
    # Match messy keys like: Landing/recently-played20260721/spotify_raw_20260721_155206.json
    # It captures the 8-digit date string attached right after the base name
    messy_pattern = re.compile(
        rf"^{re.escape(clean_base)}(\d{{8}})/(.*?spotify_raw_\1_\d{{6}}\.json)$"
    )

    paginator = s3_client.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=BUCKET_NAME)

    fixed_count = 0

    for page in pages:
        if 'Contents' not in page:
            continue

        for obj in page['Contents']:
            old_key = obj['Key']
            
            # Check if this object key has the missing slash bug
            match = messy_pattern.match(old_key)
            if match:
                date_str = match.group(1)   # e.g., "20260721"
                filename = match.group(2)   # e.g., "spotify_raw_20260721_155206.json"
                
                # Construct the CORRECT key with the slash added
                correct_key = f"{clean_base}/{date_str}/{filename}"

                print(f"Fixing:\n  OLD: {old_key}\n  NEW: {correct_key}\n")

                # 1. Copy to the corrected location
                s3_client.copy_object(
                    Bucket=BUCKET_NAME,
                    CopySource={'Bucket': BUCKET_NAME, 'Key': old_key},
                    Key=correct_key
                )

                # 2. Delete the messed up object
                s3_client.delete_object(
                    Bucket=BUCKET_NAME,
                    Key=old_key
                )
                
                fixed_count += 1

    print(f"Cleanup complete! Fixed {fixed_count} messy files.")

if __name__ == "__main__":
    # upload_file_from_local("hello.txt", f"{TARGET_BLOB_OBJECT}/hello_r2.txt")
    # list_files()
    # download_file(f"folder/hello_r2.txt", "downloaded_hello.txt")
    print(search_file_prefix('Landing/recently-played', ['20260721','20260716','20260715']))