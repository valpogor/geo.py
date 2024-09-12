import unittest
from unittest.mock import patch
import geo

class GeoTests(unittest.TestCase):

    @patch('geo.requests.get')
    def test_get_location_data_by_city(self, mock_get):
        mock_response = [{
            "name": "Beverly Hills",
            "lat": 34.0696501,
            "lon": -118.3963062
        }]
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response
        location = "Beverly Hills, California"
        result = geo.get_location_data_by_city(location, geo.apikey)
        self.assertEqual(result['name'], "Beverly Hills")
        self.assertEqual(result['lat'], 34.0696501)
        self.assertEqual(result['lon'], -118.3963062)

    @patch('geo.requests.get')
    def test_get_location_data_by_zip(self, mock_get):
        mock_response = {
            "name": "Beverly Hills",
            "lat": 34.0901,
            "lon": -118.4065
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response
        zip_code = "90210"
        result = geo.get_location_data_by_zip(zip_code, geo.apikey)
        self.assertEqual(result['name'], "Beverly Hills")
        self.assertEqual(result['lat'], 34.0901)
        self.assertEqual(result['lon'], -118.4065)

    @patch('geo.get_location_data_by_city')
    @patch('geo.get_location_data_by_zip')
    def test_handle_zip_and_city_same_location(self, mock_get_zip, mock_get_city):
        mock_get_city.return_value = {
            "name": "Beverly Hills",
            "lat": 34.0696501,
            "lon": -118.3963062
        }
        mock_get_zip.return_value = {
            "name": "Beverly Hills",
            "lat": 34.0901,
            "lon": -118.4065
        }
        city_state = "Beverly Hills, CA"
        zip_code = "90210"
        with patch('builtins.print') as mocked_print:
            geo.handle_zip_and_city(city_state, zip_code, geo.apikey)
            mocked_print.assert_called_once_with(
                "Location: Beverly Hills, Latitude: 34.0901, Longitude: -118.4065, ZIP Code: 90210")

    @patch('geo.get_location_data_by_city')
    @patch('geo.get_location_data_by_zip')
    def test_handle_zip_and_city_different_locations(self, mock_get_zip, mock_get_city):
        mock_get_city.return_value = {
            "name": "Los Angeles",
            "lat": 34.0522,
            "lon": -118.2437
        }
        mock_get_zip.return_value = {
            "name": "Beverly Hills",
            "lat": 34.0901,
            "lon": -118.4065
        }

        city_state = "Los Angeles, CA"
        zip_code = "90210"
        with patch('builtins.print') as mocked_print:
            geo.handle_zip_and_city(city_state, zip_code, geo.apikey)
            mocked_print.assert_any_call("Location: Los Angeles, Latitude: 34.0522, Longitude: -118.2437")
            mocked_print.assert_any_call(
                "Location: Beverly Hills, Latitude: 34.0901, Longitude: -118.4065, ZIP Code: 90210")

    @patch('geo.requests.get')
    def test_handle_location_by_zip(self, mock_get):
        mock_response = {
            "name": "Beverly Hills",
            "lat": 34.0901,
            "lon": -118.4065
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response
        zip_code = "90210"
        with patch('builtins.print') as mocked_print:
            geo.handle_location(zip_code, geo.apikey)
            mocked_print.assert_called_once_with(
                "Location: Beverly Hills, Latitude: 34.0901, Longitude: -118.4065, ZIP Code: 90210")

    @patch('geo.requests.get')
    def test_handle_location_by_city(self, mock_get):
        mock_response = [{
            "name": "Los Angeles",
            "lat": 34.0522,
            "lon": -118.2437
        }]
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response
        city_state = "Los Angeles, CA"
        with patch('builtins.print') as mocked_print:
            geo.handle_location(city_state, geo.apikey)
            mocked_print.assert_called_once_with("Location: Los Angeles, Latitude: 34.0522, Longitude: -118.2437")

    @patch('geo.get_location_data_by_city')
    @patch('geo.get_location_data_by_zip')
    def test_handle_invalid_city_and_zip(self, mock_get_zip, mock_get_city):
        mock_get_city.return_value = None
        mock_get_zip.return_value = None
        city_state = "Invalid City, XX"
        zip_code = "99999"
        with patch('builtins.print') as mocked_print:
            geo.handle_zip_and_city(city_state, zip_code, geo.apikey)
            mocked_print.assert_called_once_with("Failed to retrieve data for Invalid City, XX or 99999.")

if __name__ == '__main__':
    unittest.main()