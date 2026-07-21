import extract_raw_cloud_factory as factory
import r2_storage as s2_storage

TARGET_BLOB_OBJECT_RECENTLY_PLAYED='Landing/recently-played'

if __name__ == '__main__':
    factory.upload_recently_played_to_cloud(TARGET_BLOB_OBJECT_RECENTLY_PLAYED)
    # s2_storage.organize_r2_files_by_date_on_demand(TARGET_BLOB_OBJECT_RECENTLY_PLAYED)
    # s2_storage.fix_messy_r2_paths("Landing/recently-played")
    
    