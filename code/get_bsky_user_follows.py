import requests

# Base URL for the API
base_url = "https://lionsmane.us-east.host.bsky.network/xrpc/com.atproto.repo.listRecords"
did = ""

params = {
    "repo": did,
    "limit": 100,
    "collection": "app.bsky.graph.follow"
}

# Function to fetch records and handle pagination
def fetch_records():
    cursor = None
    while True:
        # Add cursor to params if it's not None
        if cursor:
            params["cursor"] = cursor

        # Make the API call
        response = requests.get(base_url, params=params)

        # Check if the request was successful
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            break

        # Parse the JSON response
        data = response.json()

        # Process the records
        records = data.get('records', [])
        for record in records:
            print(record)  # Replace with your processing logic

        # Check for the next cursor
        cursor = data.get('cursor')
        if not cursor:
            break  # No more pages, exit the loop

# Run the function
fetch_records()
