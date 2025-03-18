import os
import requests
import logging
from datetime import datetime

class WeatherService:
    def __init__(self):
        self.api_key = os.environ.get('OPENWEATHERMAP_API_KEY')
        self.base_url = 'http://api.openweathermap.org/data/2.5/weather'
        logging.basicConfig(level=logging.DEBUG)

    def get_weather(self, city, country_code='IN'):
        """Get current weather data for a location"""
        try:
            if not self.api_key:
                logging.error("OpenWeatherMap API key not found in environment variables")
                return None

            params = {
                'q': f"{city},{country_code}",
                'appid': self.api_key,
                'units': 'metric'  # Use metric units
            }

            logging.debug(f"Making weather API request for {city}, {country_code}")
            response = requests.get(self.base_url, params=params)

            if response.status_code == 401:
                logging.error("Invalid API key or unauthorized access to weather API")
                return None

            response.raise_for_status()
            data = response.json()
            logging.debug(f"Weather API response received: {data}")

            return {
                'temperature': round(data['main']['temp'], 1),
                'humidity': data['main']['humidity'],
                'description': data['weather'][0]['description'],
                'rainfall': self._get_rainfall(data),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        except requests.exceptions.RequestException as e:
            logging.error(f"Error making weather API request: {str(e)}")
            return None
        except Exception as e:
            logging.error(f"Error processing weather data: {str(e)}")
            return None

    def _get_rainfall(self, data):
        """Extract rainfall data from weather response"""
        # OpenWeatherMap provides rain data in mm for last 1 hour if available
        rain_data = data.get('rain', {}).get('1h', 0)
        return round(rain_data, 1)