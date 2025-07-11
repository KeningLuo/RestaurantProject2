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

cities = ['New York', 'San Francisco']

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
cities = ['New York', 'San Francisco']

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

# succed in Yelp

# haven't done in Foursquare