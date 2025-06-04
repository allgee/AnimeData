# etl/extract.py

import requests

def extract_data():
    print("📥 Extracting anime data from Jikan API...")

    # Define the API endpoint to fetch top anime
    url = "https://api.jikan.moe/v4/top/anime"
    response = requests.get(url)

    # If the request is successful, parse and return the data
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Retrieved {len(data.get('data', []))} anime entries.")

        # Display an example title
        if data["data"]:
            print("Example:", data["data"][0]["title"])
        return data["data"]

    # Handle failed request
    else:
        print(f"❌ Failed to retrieve data. Status code: {response.status_code}")
        return []
