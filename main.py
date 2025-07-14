# Week 2: Querying Restaurant Data
# Tasks:
# ●	Write a simple Python function to query one API (Google or Yelp).
#
# ●	Print restaurant data: name, rating, location.
#
# ●	Collect restaurant data for 2 cities (e.g., NYC and SF).
#
# Milestone:
# ●	Restaurant data for 2 cities fetched and saved as JSON files.


import requests
import pandas
import json


# fetch from Google and save as json
def fetch_restaurants(city, api_key):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        'query': f'restaurants in {city}',
        'key': api_key
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data['results']


# Replace with your Google API key
api_key = 'AIzaSyA7Tu0WvLEhi82RRGOaeti86QL5V8CVZiU'

cities = ['New York', 'San Francisco', 'Los Angeles']

for city in cities:
    print(f"\nFetching restaurants in {city}...")
    results = fetch_restaurants(city, api_key)

    # Save raw JSON results
    filename = f'Google_{city.replace(" ", "_").lower()}_restaurants.json'
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)

    # Also print basic info
    for r in results:
        name = r.get('name', 'N/A')
        rating = r.get('rating', 'N/A')
        address = r.get('formatted_address', 'N/A')
        print(f"Name: {name} | Rating: {rating} | Address: {address}")

# succeed in Google

# fetch from Yelp and save as json
import requests
import json

def fetch_yelp_restaurants(city, api_key, limit=20):
    url = "https://api.yelp.com/v3/businesses/search"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    params = {
        "term": "restaurants",
        "location": city,
        "limit": limit
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    return data.get("businesses", [])

# Replace with your real Yelp API key
yelp_api_key = "Txk6TFuWq1kMZGgBFTMLYUC11wWSyfp5mNwonT016ObyRrxmSxrrwzIjykZ6C2Ncwb8gn2PlWLTHi8O-hmdZtgVAYNl_H2Gc4XJbY1b4MbVkn9X8pp2UOiEjzAtuaHYx"
cities = ['New York', 'San Francisco', 'Los Angeles']

for city in cities:
    print(f"\nFetching restaurants from Yelp for {city}...")
    results = fetch_yelp_restaurants(city, yelp_api_key)

    # Save to JSON
    filename = f"Yelp_{city.replace(' ', '_').lower()}_restaurants.json"
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)

    # Print name, rating, address
    for r in results:
        name = r.get("name", "N/A")
        rating = r.get("rating", "N/A")
        address = ", ".join(r.get("location", {}).get("display_address", []))
        print(f"Name: {name} | Rating: {rating} | Address: {address}")

# succeed in Yelp

# haven't done in Foursquare

# Week 3: Cleaning & Saving the Data
# Tasks:
# ●	Convert JSON data to a DataFrame using pandas.
#
# ●	Standardize key fields: name, rating, price, coordinates.
#
# ●	Save to CSV.
#
# Milestone:
# ●	Cleaned and formatted CSV file with at least 100 restaurants.


import pandas as pd
import json

# load and clean Google data
def load_and_clean_google(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)

    df = pd.json_normalize(data)
    df_clean = df[[
        'name',
        'formatted_address',
        'rating',
        'price_level',
        'geometry.location.lat',
        'geometry.location.lng'
    ]].copy()

    df_clean.columns = ['name', 'address', 'rating', 'price', 'latitude', 'longitude']
    df_clean['source'] = 'google'
    return df_clean

# merge price format
def convert_price_sign_to_level(price_str):
    if isinstance(price_str, str):
        return len(price_str)  # "$$$" → 3
    return None  # missing stays as NaN

# load and clean Yelp data
def load_and_clean_yelp(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)

    df = pd.json_normalize(data)
    df_clean = df[[
        'name',
        'location.display_address',
        'rating',
        'price',
        'coordinates.latitude',
        'coordinates.longitude'
    ]].copy()

    # Convert address list to string
    df_clean['address'] = df_clean['location.display_address'].apply(lambda x: ", ".join(x))
    df_clean.drop(columns=['location.display_address'], inplace=True)

    # Convert Yelp "$" to numeric price level
    df_clean['price'] = df_clean['price'].apply(convert_price_sign_to_level)

    df_clean.columns = ['name', 'rating', 'price', 'latitude', 'longitude', 'address']
    df_clean['source'] = 'yelp'
    return df_clean


# Google JSON files
google_files = [
    'Google_new_york_restaurants.json',
    'Google_san_francisco_restaurants.json',
    'Google_los_angeles_restaurants.json'
]

# Yelp JSON files
yelp_files = [
    'Yelp_new_york_restaurants.json',
    'Yelp_san_francisco_restaurants.json',
    'Yelp_los_angeles_restaurants.json'
]

# Load and combine
google_dfs = [load_and_clean_google(file) for file in google_files]
yelp_dfs = [load_and_clean_yelp(file) for file in yelp_files]

# Merge all into one DataFrame
combined_df = pd.concat(google_dfs + yelp_dfs, ignore_index=True)

# Save as CVS
combined_df.to_csv('three cities restaurants.csv', index=False)
print("Saved all data to all_cities_combined_restaurants.csv")
