import argparse
import configparser
import requests

config = configparser.ConfigParser()
config.read('config.properties')

apikey = config.get('DEFAULT', 'apikey')
cityendpoint = config.get('DEFAULT', 'city_endpoint')
zipendpoint = config.get('DEFAULT', 'zip_endpoint')

state_code_map = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California",
    "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware", "FL": "Florida", "GA": "Georgia",
    "HI": "Hawaii", "ID": "Idaho", "IL": "Illinois", "IN": "Indiana", "IA": "Iowa",
    "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland",
    "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi", "MO": "Missouri",
    "MT": "Montana", "NE": "Nebraska", "NV": "Nevada", "NH": "New Hampshire", "NJ": "New Jersey",
    "NM": "New Mexico", "NY": "New York", "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio",
    "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina",
    "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah", "VT": "Vermont",
    "VA": "Virginia", "WA": "Washington", "WV": "West Virginia", "WI": "Wisconsin", "WY": "Wyoming"
}

def convert_state_code_to_name(location):
    if "," in location:
        city, state_code = [part.strip() for part in location.split(",")]
        if state_code in state_code_map:
            full_state_name = state_code_map[state_code]
            return f"{city},{full_state_name}"
        else:
            return location
    return location


def get_location_data_by_city(location, apikey):
    url = f'{cityendpoint}?q={location}&appid={apikey}'
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error fetching data for {location}. HTTP Status: {response.status_code}")
        return None

    data = response.json()

    if not data:
        print(f"No data found for {location}.")
        return None

    return data[0]


def get_location_data_by_zip(zip_code, apikey):
    url = f'{zipendpoint}?zip={zip_code}&appid={apikey}'
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error fetching data for ZIP code {zip_code}. HTTP Status: {response.status_code}")
        return None

    data = response.json()

    if not data:
        print(f"No data found for ZIP code {zip_code}.")
        return None

    return data


def handle_location(location, apikey):
    if location.isdigit():
        location_data = get_location_data_by_zip(location, apikey)
        if location_data:
            name = location_data.get("name", "Unknown")
            lat = location_data.get("lat", "Unknown")
            lon = location_data.get("lon", "Unknown")
            print(f"Location: {name}, Latitude: {lat}, Longitude: {lon}, ZIP Code: {location}")
        else:
            print(f"Failed to retrieve data for ZIP code {location}.")
    else:
        location_with_full_state = convert_state_code_to_name(location)
        location_data = get_location_data_by_city(location_with_full_state, apikey)
        if location_data:
            name = location_data.get("name", "Unknown")
            lat = location_data.get("lat", "Unknown")
            lon = location_data.get("lon", "Unknown")
            print(f"Location: {name}, Latitude: {lat}, Longitude: {lon}")
        else:
            print(f"Failed to retrieve data for {location}.")


def handle_zip_and_city(city_state, zip_code, apikey):
    city_data = get_location_data_by_city(convert_state_code_to_name(city_state), apikey)
    zip_data = get_location_data_by_zip(zip_code, apikey)

    if not city_data or not zip_data:
        print(f"Failed to retrieve data for {city_state} or {zip_code}.")
        return

    city_name = city_data.get("name", "Unknown")
    zip_name = zip_data.get("name", "Unknown")

    if city_name == zip_name:
        lat = zip_data.get("lat", "Unknown")
        lon = zip_data.get("lon", "Unknown")
        print(f"Location: {zip_name}, Latitude: {lat}, Longitude: {lon}, ZIP Code: {zip_code}")
    else:
        lat_city = city_data.get("lat", "Unknown")
        lon_city = city_data.get("lon", "Unknown")
        lat_zip = zip_data.get("lat", "Unknown")
        lon_zip = zip_data.get("lon", "Unknown")
        print(f"Location: {city_name}, Latitude: {lat_city}, Longitude: {lon_city}")
        print(f"Location: {zip_name}, Latitude: {lat_zip}, Longitude: {lon_zip}, ZIP Code: {zip_code}")


def main():
    parser = argparse.ArgumentParser(description="Geolocation Utility")
    parser.add_argument('locations', nargs='+', help="List of locations in the format 'City, State' or zip code")
    parser.add_argument('--appid', required=False,
                        help="OpenWeatherMap API Key (optional, overrides config.properties)")

    args = parser.parse_args()
    api_key = args.appid if args.appid else apikey
    locations = args.locations

    i = 0
    while i < len(locations):
        loc1 = locations[i]
        if i + 1 < len(locations) and locations[i + 1].isdigit():
            handle_zip_and_city(loc1, locations[i + 1], api_key)
            i += 2
        else:
            handle_location(loc1, api_key)
            i += 1


if __name__ == '__main__':
    main()
