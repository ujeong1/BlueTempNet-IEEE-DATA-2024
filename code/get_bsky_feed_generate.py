import time
import json
import pandas as pd
from atproto import Client, models
from tqdm import tqdm


def post_to_dict(post_obj):
    """Convert post object to dictionary excluding private attributes."""
    return {x: str(post_obj[x]) for x in dir(post_obj) if '_' not in x}


def post_to_author(post_obj):
    """Extract author handle from the post object."""
    return post_obj["author"]["handle"]


def profile_to_dict(profile_obj):
    """Convert profile object to dictionary excluding private attributes."""
    return {x: str(profile_obj[x]) for x in dir(profile_obj) if '_' not in x}


def profile_to_key_dict(profile_obj):
    """Convert profile object to dictionary using the model fields."""
    result = {}
    keys = profile_obj["model_fields_set"]
    for key in keys:
        result[key] = str(profile_obj[key])
    return result


# Initialize client and login
client = Client()
client.login('USERNAME', 'PASSWORD')

feed_uris = []

# Rate limit parameters
max_requests_per_5min = 3000
time_window = 300  # 5 minutes in seconds
delay_between_requests = time_window / max_requests_per_5min  # Average time per request

# Process each feed URL and extract feed generator profiles
for input_handle in feed_uris:
    try:
        params = models.AppBskyFeedGetFeedGenerator.Params(feed=input_handle)
        response = client.app.bsky.feed.get_feed_generator(params)
        
        # Convert feed profile to dictionary
        feed_profile = response['view']
        feed_profile = profile_to_key_dict(feed_profile)
        profiles[input_handle] = feed_profile

    except Exception as e:
        print(f"Error processing {input_url}: {e}")
        missed_count += 1
        continue

    # Sleep to respect rate limits
    time.sleep(delay_between_requests)

# Save the profiles to a JSON file
with open("list_profiles.json", "w") as f:
    json.dump(profiles, f)
