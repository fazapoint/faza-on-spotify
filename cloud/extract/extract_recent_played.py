import extract_raw_cloud_factory as factory

TARGET_BLOB_OBJECT_RECENTLY_PLAYED='Landing/recently-played'

if __name__ == '__main__':
    factory.upload_recently_played_to_cloud(TARGET_BLOB_OBJECT_RECENTLY_PLAYED)
    