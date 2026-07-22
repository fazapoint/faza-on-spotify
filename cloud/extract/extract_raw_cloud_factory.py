import os
from dotenv import load_dotenv
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime, timezone, timedelta
from r2_storage import upload_file_from_api
from pathlib import Path


# load credential from .env
load_dotenv()

# basedir
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Go up two levels to get to the absolute project root (/root)
ROOT_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))
CACHE_PATH = os.path.join(ROOT_PATH, ".cache")

def get_date_only():
    WIB = timezone(timedelta(hours=7))
    today_date = datetime.now(WIB).strftime("%Y%m%d")
    return today_date

def get_datetime():
    WIB = timezone(timedelta(hours=7))
    timestamp = datetime.now(WIB).strftime("%Y%m%d_%H%M%S")
    return timestamp

def generate_filename(target_storage):
    base_dir = Path(target_storage)
    filename = (base_dir / get_date_only() / f"spotify_raw_{get_datetime()}.json").as_posix()
    return filename

# setup auth
scope = "user-read-recently-played" # scope from auth spotify api
auth_manager = SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope=scope,
    open_browser=False, # Safer for terminal usage
    cache_path=CACHE_PATH # add cache login
)
sp = spotipy.Spotify(auth_manager=auth_manager)

def get_latest_recently_played_file(target_storage):
    result = generate_filename(target_storage)
    print(result)


def upload_recently_played_to_cloud(target_storage):
    print("Fetching xxx data............")

    filename = generate_filename(target_storage)
    # print(filename)
    try:
        # fetch the data
        results = sp.current_user_recently_played()
        json_string = json.dumps(results, indent=4, ensure_ascii=False)

        # upload to r2 storage
        upload_file_from_api(json_string, filename)

        print("Extract completed............")

    except Exception as e:
        print(f"Error: {e}")
        raise

if __name__ == '__main__':
    # upload_recently_played_to_cloud("Landing/recently-played")
    # get_latest_recently_played_file("test")
