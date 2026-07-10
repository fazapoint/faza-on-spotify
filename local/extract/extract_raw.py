import os
from dotenv import load_dotenv
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime, timezone, timedelta

# load credential from .env
load_dotenv()

# 1. Get the directory where this script lives (/root/local/extract)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. Go up two levels to get to the absolute project root (/root)
ROOT_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))

# 3. Build everything cleanly going DOWN from ROOT_PATH
LANDING_PATH = os.path.join(ROOT_PATH, "local", "Warehouse", "Landing")
LANDING_RECENTLY_PLAYED = os.path.join(LANDING_PATH, "Landing_Recently_Played")
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

# output
print("Fetching xxx data .....")

# Create a filename with today's date/time
# This prevents overwriting and creates a history in your folder
WIB = timezone(timedelta(hours=7))
timestamp = datetime.now(WIB).strftime("%Y%m%d_%H%M%S")
filename = os.path.join(LANDING_RECENTLY_PLAYED, f"spotify_raw_{timestamp}.json")

# Initialize an empty folder if it doesnt exist
if not os.path.exists(LANDING_RECENTLY_PLAYED):
    os.makedirs(LANDING_RECENTLY_PLAYED, exist_ok=True)

try:
    # fetch the data
    results = sp.current_user_recently_played()

    # Save to local file
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    print(f"Successfully saved {len(results['items'])} tracks to {filename}!")

except Exception as e:
    print(f"Error: {e}")
