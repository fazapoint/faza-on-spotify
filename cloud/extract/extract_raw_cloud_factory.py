import os
from dotenv import load_dotenv
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime, timezone, timedelta
from r2_storage import upload_file_from_api


# load credential from .env
load_dotenv()

# basedir
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Go up two levels to get to the absolute project root (/root)
ROOT_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))
CACHE_PATH = os.path.join(ROOT_PATH, ".cache")

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


def upload_recently_played_to_cloud(target_storage):
    print("Fetching xxx data............")

    # generate filename
    WIB = timezone(timedelta(hours=7))
    timestamp = datetime.now(WIB).strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(target_storage, f"spotify_raw_{timestamp}.json")

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
    upload_recently_played_to_cloud("path_to_storage_blob")
