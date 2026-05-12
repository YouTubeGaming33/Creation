# Directory of Helper Commands for Requesting Data etc...

# Required Import(s)
import requests

# Helper Function for Pulling Online Users from Minecraft Server.
def pull_users():
    server_address = "mc.jamswert.top"
    # Use api.mcsrvstat.us
    response = requests.get(f"https://api.mcsrvstat.us/3/{server_address}")
    data = response.json()

    if data.get('online'):
        # Access the players dictionary
        players_data = data.get('players', {})
        
        # Check if the 'list' exists (some servers hide this)
        if 'list' in players_data:
            # Use a list comprehension to grab just the 'name' from every player object
            usernames = [player['name'] for player in players_data['list']]
            return usernames
    return []

# Helper Function for Pulling Server Status (Offline/Online).
def pull_status():
    server_address = "mc.jamswert.top"
    response = requests.get(f"https://api.mcsrvstat.us/3/{server_address}")
    data = response.json()
    print("Data Pulled")
    return data