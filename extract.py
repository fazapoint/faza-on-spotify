import os
from dotenv import load_dotenv
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime

# load credential from .env
load_dotenv()

# setup auth
scope = "user-read-recently-played"
auth_manager = SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope=scope,
    open_browser=False # Safer for terminal usage
)
sp = spotipy.Spotify(auth_manager=auth_manager)

# output
print("Fetching xxx data .....")

# Define the directory and ensure it exists
base_folder = os.path.join("data", "L1", "spotify")
os.makedirs(base_folder, exist_ok=True)

# Create a filename with today's date/time
# This prevents overwriting and creates a history in your folder
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = os.path.join(base_folder, f"spotify_raw_{timestamp}.json")

try:
    # fetch the data
    results = sp.current_user_recently_played(limit=2)

    # Save to local file
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    print(f"Successfully saved {len(results['items'])} tracks to {filename}!")

except Exception as e:
    print(f"Error: {e}")