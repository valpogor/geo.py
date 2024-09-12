# Geolocation Utility

A Python command-line tool that fetches geographical location data (latitude, longitude, and place name) based on
city/state and/or zip code
using the [OpenWeatherMap API](https://openweathermap.org/api/geocoding-api#direct_name). The utility now supports
comparing results from city/state and zip codes and returning only zip code data
when both point to the same location.

## Features

- Fetch geographical coordinates (latitude and longitude) and place name using city and state.
- Fetch geographical data using a zip code.
- If both city/state and zip code refer to the same location, only the zip code result is shown.
- Command-line interface for easy interaction.
- Unit tests

## Requirements

- Python 3.6+
- `requests` library (install using `pip install requests`)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/valpogor/geo.py.git
    ```

2. Navigate into the project directory:
    ```bash
    cd geo.py
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Fetch data using City and State

```bash
python geo.py "Madison, WI"
```

### Fetch data using City, State, and Zip Code (same location)

If the city/state and zip code refer to the same location, the utility will return only the result for the zip code.

```bash
python geo.py "Schenectady, NY" "12345"
```

Output:

```bash
Location: Schenectady, Latitude: 42.8142, Longitude: -73.9396, ZIP Code: 12345
```

### Fetch data using City, State, and Zip Code (different locations)

If the city/state and zip code refer to different locations, the utility will return both results.

```bash
python geo.py "New York, NY" "10001"
```

Output:

```bash
Location: New York, Latitude: 40.7128, Longitude: -74.0060
Location: Albany, Latitude: 42.6526, Longitude: -73.7562, ZIP Code: 10001
```

### Fetch data using multiple locations (City/State and Zip Code combinations)

```bash
python geo.py "Madison, WI" "12345" "Chicago, IL" "60601"
```

### Fetch data using a single Zip Code

```bash
python geo.py "12345"
```

## Unit Testing

Unit tests for the utility are provided in the `geotests.py` file.

### Running the Tests

Run the following command to execute the tests:

```bash
python -m unittest tests/geotests.py
```

### Test Scenarios Covered:

1. Fetching data by city/state.
2. Fetching data by zip code.
3. Fetching data by both city/state and zip code (same location).
4. Fetching data by both city/state and zip code (different locations).
5. Handling invalid city/state and zip code.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
