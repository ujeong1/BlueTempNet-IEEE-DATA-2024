import time
import re
import json
from atproto import Client, CAR, models


def post_to_dict(post_obj):
    return {x: str(post_obj[x]) for x in dir(post_obj) if '_' not in x}


def post_to_author(post_obj):
    return post_obj["author"]["handle"]


def profile_to_dict(profile_obj):
    return {x: str(profile_obj[x]) for x in dir(profile_obj) if '_' not in x}


def profile_to_key_dict(profile_obj):
    result = {}
    keys = profile_obj["model_fields_set"]
    for key in keys:
        result[key] = str(profile_obj[key])
    return result


client = Client()
client.login('USERNAME', 'PASSWORD')
feed_uris = []
friends = {}
limit = 100

# Rate limit parameters
max_requests_per_5min = 3000
time_window = 300  # 5 minutes in seconds
delay_between_requests = time_window / max_requests_per_5min  # Average time per request

for input_handle in feed_uris:
    cursor = None
    like_profiles = []
    request_count = 0

    while True:
        try:
            response = client.get_likes(input_handle, cursor=cursor, limit=limit)
            likes = response['likes']
            request_count += 1

            # Process likes if any
            if likes:
                like_profiles += [profile_to_key_dict(profile_obj) for profile_obj in likes]

            # Check for pagination
            cursor = response.cursor
            if not cursor:
                break

            # Sleep to respect rate limit
            if request_count >= max_requests_per_5min:
                print("Reached maximum requests in the time window. Sleeping for 5 minutes...")
                time.sleep(time_window)  # Sleep for 5 minutes
                request_count = 0  # Reset request count after sleeping
            else:
                time.sleep(delay_between_requests)  # Sleep for average time per request

        except Exception as e:
            print(f"An error occurred: {e}")
            if 'rate limit' in str(e).lower():  # Handle specific rate limit error
                print("Rate limit reached. Sleeping for 5 minutes...")
                time.sleep(time_window)  # Sleep for 5 minutes
                request_count = 0  # Reset request count after sleeping
            else:
                break  # Break the loop for other exceptions

    friends[input_handle] = like_profiles

# Save results to JSON file
with open("list_likes_times_within_time.json", "w") as f:
    json.dump(friends, f)
